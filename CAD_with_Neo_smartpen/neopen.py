from __future__ import print_function
from bluepy.btle import *
#import bluepy.btle
import struct
import time


def isNeoPen(dev):
    for adtype, desc, value in dev.getScanData():
        if desc == 'Complete Local Name' and (value == 'Neosmartpen_M1' or value == 'Neosmartpen_N2'):
            return True
    return False


class NotificationHandler(DefaultDelegate):
    def handleNotification(self, cHandle, data):
        # print("Notification: %s %s" % (len(data),data.encode('hex'))) #len(data)))# data.encode('hex')))
        packets = data.split(b'\xc1')
        for pkt in packets:
            if not pkt:
                continue
            if not pkt.startswith('\xc0'):
                print("Possible malformed packet %s?" % pkt.encode('hex'))
                continue
            pkt = pkt.rstrip(b'\xc1')
            pkt = pkt.replace('\x7d\xe1', '\xc1').replace(
                '\x7d\xe0', '\xc0').replace('\x7d\x5d', '\x7d')
            pen_Msg = pkt.encode('hex')
            
            # print(pen_Msg)
            if (pen_Msg[0:2] == 'c0' and pen_Msg[2:4] == '6c' or pen_Msg[2:4] == '65'):
                Dot_Decod(pen_Msg,pkt)
                # if (len(pkt)==17):
                #     print(struct.unpack('<BBBBBHHHBBBBH',pkt))

            if (pen_Msg[0:2] == 'c0' and pen_Msg[2:4] == '63'):
                #print("pen_up_down info",pen_Msg[9:10])
                if(pen_Msg[9:10] == '0'):
                    print("lift=down")
                elif(pen_Msg[9:10] == '1'):
                    print("lift=up")


def make_packet(opcode, contents):
    contents = chr(opcode) + struct.pack('<h', len(contents)) + contents
    contents.replace('\x7d', '\x7d\x5d').replace(
        '\xc0', '\x7d\xe0').replace('\xc1', '\x7d\xe1')
    return '\xc0' + contents + '\xc1'


def send_packet(Msg, outchar):
    div_Pack = 5
    chunck, chunck_size = len(Msg), len(Msg)//div_Pack
    Msg_p = [Msg[i:i+chunck_size]for i in range(0, chunck, chunck_size)]
    #outchar.write(Msg, withResponse=True)
    for i in range(0, div_Pack-1):
        outchar.write(Msg_p[i])
    outchar.write(Msg_p[div_Pack], withResponse=True)


def Dot_Decod(msg,pkt):

    if (len(pkt)==17):
        read_out = (struct.unpack('<BBBBBHHHBBBBH',pkt))
        x = read_out[6]*100+read_out[8]
        y = read_out[7]*100+read_out[9]
        force = read_out[5]
        twist = read_out[12]
        tau_X=read_out[10]
        tau_Y=read_out[11]

        print("x:%i y:%i force: %i, twist: %i, Tau_x: %i,Tau_y:%i"% (x/4.375, y/4.375, force, twist*2, tau_X,tau_Y))

    # x = (int(msg[14:16], 16))*100+(int(msg[22:24], 16))  # X coordinate +fx
    # y = (int(msg[18:20], 16))*100+(int(msg[24:26], 16))  # Y coordinate +fy
    # force = (int(msg[12:14], 16))*256+(int(msg[10:11], 16)) * \
    #     16+(int(msg[9:10], 16))  # pressure

    # data1=[int(msg[2*i:2*i+2],16) for i in range(len(msg)/2)]
    # print(data1)
        
    # if force < 1000:
    #     print("x:%i y:%i force: %i" % (x//4.375, y/4.375, force))


def runNeoPen(dev):
    p = Peripheral(dev.addr, ADDR_TYPE_RANDOM).withDelegate(
        NotificationHandler())
    p.setMTU(102)
    chars = None
    for svc in p.getServices():
        if svc.uuid.getCommonName() == 'Device Information':
            print("Device info:")
            for char in svc.getCharacteristics():
                print("  %s = %s" % (char.uuid.getCommonName(), char.read()))
        elif svc.uuid.getCommonName() == '19f1':
            print("Found NeoPen vendor service")
            chars = {char.uuid.getCommonName(
            ): char for char in svc.getCharacteristics()}

    if chars is None:
        raise Exception("Did not find vendor service!")

    # enable notifications
    inchar = chars['2ba1']
    p.writeCharacteristic(inchar.valHandle + 1, '\x01\x00', withResponse=True)
    outchar = chars['2ba0']

    # setup: VERSION_REQUEST
    print("Sending version message...")
    msg = make_packet(0x01, '\x00' * 16 + '\x12\x01' +
                      '2.1.8.0'.ljust(16, '\0') + '2.12'.ljust(8, '\0'))
    send_packet(msg, outchar)
    #outchar.write(msg, withResponse=True)
    time.sleep(0.50)
    # setup: SETTING_INFO_REQUEST (pre-authentication)
    msg = make_packet(0x04, '')
    outchar.write(msg, withResponse=True)
    time.sleep(0.50)

    #outchar.write(make_packet(0x05, '\x08\xf0\x6b\x3c\x00'), withResponse=True)
    # outchar.write(make_packet(0x05, '\x08\x00\x00\x00\x00\x00'),
    #               withResponse=True)    
    # msg = make_packet(0x04, '')
    # outchar.write(msg, withResponse=True)
    # time.sleep(0.50)
    # beep setting off then on again to make it beep audibly now
    outchar.write(make_packet(0x05, '\x05\x00'), withResponse=True)
    outchar.write(make_packet(0x05, '\x05\x01'), withResponse=True)
    
    # hover mode enable
    outchar.write(make_packet(0x05, '\x06\x01'), withResponse=True)
    
    # color change try
    # outchar.write(make_packet(0x05, '\x08\xdd\xdd\x30\x40\x70'), withResponse=True)

    # msg = make_packet(0x04, '')
    # outchar.write(msg, withResponse=True)
    # time.sleep(0.50)

    # setup: ONLINE_DATA_REQUEST
    outchar.write(make_packet(0x11, '\xff\xff'), withResponse=True)

    # for i in range(1):
    #     outchar.write(make_packet(0x05, '\x05\x00'), withResponse=True)
    #     outchar.write(make_packet(0x05, '\x05\x01'), withResponse=True)
    #     time.sleep(0.5)

    # setup: OFFLINE_NOTE_LIST_REQUEST
#	outchar.write(make_packet(0x21, '\xff\xff\xff\xff'), withResponse=True)
#	time.sleep(0.50)
    # setup: SETTING_INFO_REQUEST (post-authentication - real status request)
    msg = make_packet(0x04, '')
    outchar.write(msg, withResponse=True)
#	time.sleep(0.50)
    # SETTING_CHANGE_REQUEST: DataTransmissionType (14) = Event (0)
    outchar.write(make_packet(0x05, '\x0e\x00'), withResponse=True)
#	time.sleep(0.50)

    while True:
        try:
            p.waitForNotifications(1.0)
        except BTLEDisconnectError:
            print("Pen disconnected!")
            return


scanner = Scanner()
while 1:
    print("Scanning...")
    devices = scanner.scan(2.0)

    for dev in devices:
        if isNeoPen(dev):
            print("Found available NeoPen %s, connecting..." % (dev.addr))
            runNeoPen(dev)

    scanner.clear()
