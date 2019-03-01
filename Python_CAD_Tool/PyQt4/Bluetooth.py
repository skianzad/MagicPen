from __future__ import print_function
from bluepy.btle import *
#import bluepy.btle
import struct
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *

X_coord = 0
Y_coord = 0
force = 0
	
def isNeoPen(dev):
	for adtype, desc, value in dev.getScanData():
		if desc == 'Complete Local Name' and value == 'Neosmartpen_M1':
			return True
	return False
	
		
def make_packet(opcode, contents):
		contents = chr(opcode) + struct.pack('<h', len(contents)) + contents
		contents.replace('\x7d', '\x7d\x5d').replace('\xc0', '\x7d\xe0').replace('\xc1', '\x7d\xe1')
		return '\xc0' + contents + '\xc1'
		
def send_packet(Msg, outchar):
	div_Pack=5
	chunck, chunck_size=len(Msg),len(Msg)//div_Pack
	Msg_p=[Msg[i:i+chunck_size]for i in range(0,chunck,chunck_size)]
	#outchar.write(Msg, withResponse=True)
	for i in range(0,div_Pack-1):
		outchar.write(Msg_p[i])
	outchar.write(Msg_p[div_Pack], withResponse=True)


class NotificationHandler(DefaultDelegate):
	def handleNotification(self, cHandle, data):
		# print("Notification: %s %s" % (cHandle,data.encode('hex'))) #len(data)))# data.encode('hex')))
		pen_Msg=data.encode('hex')
		if (pen_Msg[0:2]=='c0' and pen_Msg[2:4]=='6c' or pen_Msg[2:4]=='65'):
			self.Dot_Decod(pen_Msg)
		
	def Dot_Decod(self, msg):
		global X_coord, Y_coord, force
		x=(int(msg[14:16],16))*100+(int(msg[22:24],16)) # X coordinate +fx
		y=(int(msg[18:20],16))*100+(int(msg[24:26],16)) # Y coordinate +fy
		force=(int(msg[12:14],16))*256+(int(msg[10:11],16))*16+(int(msg[9:10],16)) # pressure
		if force <1000:
			X_coord = x/4.375
			Y_coord = y/4.375
			force = force
			# print("x:%i y:%i force: %i" % (x/4.375,y/4.375,force))	
			
		
class BluetoothThread(QThread):	
	sigOut = pyqtSignal(list)
		
	def runNeoPen(self, dev):
		global X_coord, Y_coord, force
	
		p = Peripheral(dev.addr, ADDR_TYPE_RANDOM).withDelegate(NotificationHandler())
		p.setMTU(40)
		chars = None
		for svc in p.getServices():
			if svc.uuid.getCommonName() == 'Device Information':
				print("Device info:")
				for char in svc.getCharacteristics():
					sys.stdout.write("  %s = %s" % (char.uuid.getCommonName(), char.read()))
					pass
			elif svc.uuid.getCommonName() == '19f1':
				print("Found NeoPen vendor service")
				chars = {char.uuid.getCommonName(): char for char in svc.getCharacteristics()}

		if chars is None:
			raise Exception("Did not find vendor service!")

		# enable notifications
		inchar = chars['2ba1']
		p.writeCharacteristic(inchar.valHandle + 1, '\x01\x00', withResponse=True)
		outchar = chars['2ba0']

		# setup: VERSION_REQUEST
		print("Sending version message...")
		msg = make_packet(0x01, '\x00' * 16 + '\x12\x01' + '2.1.8.0'.ljust(16, '\0') + '2.12'.ljust(8, '\0'))
		send_packet(msg,outchar)
		#outchar.write(msg, withResponse=True)
		time.sleep(0.50)
		# setup: SETTING_INFO_REQUEST (pre-authentication)
		msg = make_packet(0x04, '')
		outchar.write(msg, withResponse=True)
		time.sleep(0.50)

		#outchar.write(make_packet(0x05, '\x08\xf0\x6b\x3c\x00'), withResponse=True)
		outchar.write(make_packet(0x05, '\x08\x00\x00\x00\x00\x00'), withResponse=True)
		outchar.write(make_packet(0x05, '\x05\x01'), withResponse=True)

		# setup: ONLINE_DATA_REQUEST
		outchar.write(make_packet(0x11, '\xff\xff'), withResponse=True)
		# setup: OFFLINE_NOTE_LIST_REQUEST
		#	outchar.write(make_packet(0x21, '\xff\xff\xff\xff'), withResponse=True)
		#	time.sleep(0.50)
			# setup: SETTING_INFO_REQUEST (post-authentication - real status request)
		#	msg = make_packet(0x04, '')
		#	outchar.write(msg, withResponse=True)
		#	time.sleep(0.50)
			# SETTING_CHANGE_REQUEST: DataTransmissionType (14) = Event (0)
		#	outchar.write(make_packet(0x05, '\x0e\x00'), withResponse=True)
		#	time.sleep(0.50)

		while True:
			dataList = [X_coord, Y_coord, force]
			self.sigOut.emit(dataList)
			# print(dataList)
			p.waitForNotifications(1.0)


    # overwrite  the run method to continously receive data from the socket
	def run(self):
		scanner = Scanner()
		while 1:
			print("Scanning...")
			devices = scanner.scan(2.0)

			for dev in devices:
				if isNeoPen(dev):
					print("Found available NeoPen %s, connecting..." % (dev.addr))
					self.runNeoPen(dev)
					

			scanner.clear()


