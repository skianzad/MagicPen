package main

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"time"

	"tinygo.org/x/bluetooth"
)

var adapter = bluetooth.DefaultAdapter

const (
	deviceNameUUID = 0x180A
)

type penState struct {
	x float64
	y float64
	force float64
	lifted bool
}

func (ps penState) String() string {
	return fmt.Sprintf("x: %v | y: %v | force: %v | lifted?: %v", ps.x, ps.y, ps.force, ps.lifted)
}

func main() {
	 // Enable BLE interface.
	must("enable BLE stack", adapter.Enable())

	stateChan := make(chan penState) // Buf length

	// Start scanning.
	println("scanning...")
	err := adapter.Scan(func(adapter *bluetooth.Adapter, device bluetooth.ScanResult) {
		println("found device:", device.Address.String(), device.RSSI, device.LocalName())
		if (isNeopen(device)) {
			err := adapter.StopScan()
			if err != nil {
				panic(err)
			}

			err = initPen(adapter, device, stateChan)
			if err != nil {
				panic(err)
			}
		}
	})
	must("start scan", err)

	for state := range stateChan {
		fmt.Println(state)
	}
}

func must(action string, err error) {
	if err != nil {
		panic("failed to " + action + ": " + err.Error())
	}
}

func isNeopen(device bluetooth.ScanResult) bool {
	return device.LocalName() == "Neosmartpen_M1" || device.LocalName() == "Neosmartpen_N2"
}

func initPen(adapter *bluetooth.Adapter, device bluetooth.ScanResult, stateChan chan penState) error {
	dev, err := adapter.Connect(device.Address, bluetooth.ConnectionParams {})
	if err != nil {
		return err
	}

	println("Connected to neopen")

	services, err := dev.DiscoverServices(nil)
	if err != nil {
		return err
	}

	chars := make(map[uint32] bluetooth.DeviceCharacteristic)

	println("Discovering services")

	for _, service := range services {
		if (service.UUID()[3] == deviceNameUUID) {
			println("Device Info:")
			characteristics, err := service.DiscoverCharacteristics(nil)
			if err != nil {
				return err
			}

			for _, characteristic := range characteristics {
				var buf []byte
				characteristic.Read(buf)
				fmt.Printf("%X = %v\n", characteristic.UUID()[3], buf)
			}

		} else if (service.UUID()[3] == 0x19f1) {
			println("Found NeoPen vendor service")

			characteristics, err := service.DiscoverCharacteristics(nil)
			if err != nil {
				return err
			}

			for _, characteristic := range characteristics {
				chars[characteristic.UUID()[3]] = characteristic
			}
		}
	}

	fmt.Println(chars)

	for k, v := range chars {
		fmt.Printf("%X : %v\n", k, v)
	}

	////////////////
	// MAGIC TIME //
	////////////////

	println("Magic time!!!")

	inchar := chars[0x2BA1]

	err = inchar.EnableNotifications(createPenDataHandler(stateChan))
	if err != nil {
		return err
	}

	outchar := chars[0x2BA0]

	outchar.EnableNotifications(func(buf []byte) { println("outchar notification") })

	// May have to write to inchar here as on line 126 api.py
	// outchar.WriteWithoutResponse([]byte("\xc0\x01*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x012.1.8.0\x00\x00\x00\x00\x00\x00\x00\x00\x002.12\x00\x00\x00\x00\xc1"))

	// May have to write version message to outchar here as on line 132-133 api.py

	// SETTING INFO REQUEST?
	_, err = outchar.WriteWithoutResponse(makePacket(0x04, []byte{}))
	if err != nil {
		return err
	}

	time.Sleep(time.Second / 4)

	_, err = outchar.WriteWithoutResponse(makePacket(0x05, []byte{0x08, 0xF0, 0x6B, 0x3C, 0x00}))
	if err != nil {
		return err
	}
	time.Sleep(time.Second / 4)

	_, err = outchar.WriteWithoutResponse(makePacket(0x05, []byte{0x05, 0x01}))
	if err != nil {
		return err
	}
	time.Sleep(time.Second / 4)

	_, err = outchar.WriteWithoutResponse(makePacket(0x05, []byte{0x05, 0x00}))
	if err != nil {
		return err
	}
	time.Sleep(time.Second / 4)

	_, err = outchar.WriteWithoutResponse(makePacket(0x05, []byte{0x05, 0x01}))
	if err != nil {
		return err
	}
	time.Sleep(time.Second / 4)

	_, err = outchar.WriteWithoutResponse(makePacket(0x05, []byte{0x06, 0x01}))
	if err != nil {
		return err
	}
	time.Sleep(time.Second / 4)

	_, err = outchar.WriteWithoutResponse(makePacket(0x11, []byte{0xFF, 0xFF}))
	if err != nil {
		return err
	}
	time.Sleep(time.Second / 4)

	// Beeping?????
	_, err = outchar.WriteWithoutResponse(makePacket(0x05, []byte{0x05, 0x00}))
	if err != nil {
		return err
	}
	time.Sleep(time.Second / 4)

	_, err = outchar.WriteWithoutResponse(makePacket(0x05, []byte{0x05, 0x01}))
	if err != nil {
		return err
	}
	time.Sleep(time.Second / 4)

	return nil
}

func createPenDataHandler(stateChan chan penState) func([]byte) {
	return func(buf []byte) {
		// fmt.Printf("Data: %v\n", buf)

		penLiftedNext := true

		for _, packet := range bytes.Split(buf, []byte{0xC1}) {
			if len(packet) == 0 {
				continue
			} else if packet[0] != 0xC0 {
				// Malformed packet
				continue
			}

			packet = bytes.TrimRight(packet, "\xC1")
			packet = bytes.ReplaceAll(packet, []byte{0x7D, 0xE1}, []byte{0xC1})
			packet = bytes.ReplaceAll(packet, []byte{0x7D, 0xE0}, []byte{0xC0})
			packet = bytes.ReplaceAll(packet, []byte{0x7D, 0x5D}, []byte{0x7D})

			// fmt.Printf("Packet: %v\n", packet)

			// This grouping might be wrong, it could be (0xC0 and 0x6C) or 0x65
			if (packet[0] == 0xC0 && packet[1] == 0x6C) || packet[1] == 0x65 {
				if (len(packet) == 17) {
					state := decode(packet)
					if penLiftedNext {
						state.force = 0
						state.lifted = true
						penLiftedNext = false
					}
					// Only send state if someone wants it. This ensures that reading from the
					// channel will always result in the most up to date state.
					select {
					case stateChan <- state:
					default:
					}
				}
			} else if packet[0] == 0xC0 && packet[1] == 0x63 {
				switch packet[5] & 0x5 {
				case 0: penLiftedNext = false
				case 1: penLiftedNext = true
				default:
				}
			}
		}
	}
}

func decode(packet []byte) penState {
	// Even more magic!!

	decode := binary.LittleEndian

	var state penState

	x := decode.Uint16(packet[7:9]) * 100 + uint16(packet[11])
	y := decode.Uint16(packet[9:11]) * 100 + uint16(packet[12])

	force := decode.Uint16(packet[5:7])

	// twist := decode.Uint16(packet[15:17])

	// tau_X := packet[13]
	// tau_y := packet[14]

	state.x = 0.175 * float64(x) / 4.375
	state.y = 0.175 * float64(y) / 4.375
	state.force = float64(force) / 4
	state.lifted = false

	return state
}

// This assumes buf as len <= 255, which it does in all cases in api.py
func makePacket(opcode byte , buf []byte) []byte {
	buf = append([]byte{opcode, byte(len(buf)), 0x00}, buf...)
	buf = bytes.ReplaceAll(buf, []byte{0x7D}, []byte{0x7D, 0x5D})
	buf = bytes.ReplaceAll(buf, []byte{0xC0}, []byte{0x7D, 0xE0})
	buf = bytes.ReplaceAll(buf, []byte{0xC1}, []byte{0x7D, 0xE1})

	buf = append([]byte{0xC0}, append(buf, 0xC1)...)

	fmt.Printf("Encoded packet: %v\n", buf)

	return buf
}
