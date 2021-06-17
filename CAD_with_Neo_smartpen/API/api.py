from __future__ import print_function
from bluepy.btle import *
#import bluepy.btle
import struct
import time
# from PyQt4.QtGui import       *
# from PyQt4.QtCore import *
import logging
import binascii

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
X_coord = 0
Y_coord = 0
force = 0
pen_Code = 0
global lifted
lifted= False
flag =  False

FORCE_HOVERING_MAX = 5.0 # max force a user can apply on pen tip while hovering

def asUtf8(s):
	return bytes(s, 'raw_unicode_escape')
	# return bytes(s) # python2

def isNeoPen(dev):
	for adtype, desc, value in dev.getScanData():
		if desc == 'Complete Local Name' and (value == 'Neosmartpen_M1' or value == 'Neosmartpen_N2'):
			return True
	return False

def make_packet(opcode, contents):
	contents = bytes([opcode]) + struct.pack('<h', len(contents)) + asUtf8(contents)
	contents.replace( asUtf8('\x7d')
			, asUtf8('\x7d\x5d')).replace(asUtf8('\xc0')
			, asUtf8('\x7d\xe0')).replace(asUtf8('\xc1')
			, asUtf8('\x7d\xe1') )
	contents = asUtf8('\xc0') + contents + asUtf8('\xc1')
	# print(binascii.hexlify(contents)) # debug
	return contents

		
def send_packet(Msg, outchar):
	div_Pack=4
	chunck, chunck_size=len(Msg),len(Msg)//div_Pack
	Msg_p=[Msg[i:i+chunck_size]for i in range(0,chunck,chunck_size)]
	#outchar.write(Msg, withResponse=True)
	for i in range(0,div_Pack-1):
		outchar.write(Msg_p[i])
	outchar.write(Msg_p[div_Pack], withResponse=True)


class NotificationHandler(DefaultDelegate):
	def handleNotification(self, cHandle, data):
		global lifted , flag

		# print("Notification: %s %s" % (cHandle,data.encode('hex'))) #len(data)))# data.encode('hex')))
		packets = data.split(b'\xc1')
		for pkt in packets:
			if not pkt:
				continue
			if not pkt.startswith(asUtf8('\xc0')):
				print("Possible malformed packet %s?" % pkt.encode('hex'))
				continue
			pkt = pkt.rstrip(b'\xc1')
			pkt = pkt.replace(asUtf8('\x7d\xe1'), asUtf8('\xc1')).replace(asUtf8('\x7d\xe0'), asUtf8('\xc0')).replace(asUtf8('\x7d\x5d'), asUtf8('\x7d'))
			pen_Msg = pkt.hex()
			# pen_Msg = pkt.encode('hex') # python2
			# print(pen_Msg)
			if (pen_Msg[0:2]=='c0' and pen_Msg[2:4]=='6c' or pen_Msg[2:4]=='65'):
				self.Dot_Decod(pen_Msg,pkt)
			if (pen_Msg[0:2]=='c0' and pen_Msg[2:4]=='63'):
				if(pen_Msg[9:10]=='0'):
					lifted  =       False                           
				if(pen_Msg[9:10]=='1'):
					lifted  =       True
					force   =       0
			
	def Dot_Decod(self, msg,pkt):
		global X_coord, Y_coord, force
		if (len(pkt)==17):
			read_out = (struct.unpack('<BBBBBHHHBBBBH',pkt))
			x = read_out[6]*100+read_out[8]
			y = read_out[7]*100+read_out[9]
			force = read_out[5]
			twist = read_out[12]
			tau_X=read_out[10]
			tau_Y=read_out[11]
			# print("x:%i y:%i force: %i, twist: %i, Tau_x: %i,Tau_y:%i"% (x/4.375, y/4.375, force, twist*2, tau_X,tau_Y))
			X_coord = .175*x/4.375
			Y_coord = .175*y/4.375
			force = force/4.0
			#print("x:%i y:%i force: %i" % (x/4.375,y/4.375,force)) 
			
		
def initPen(dev):
	global X_coord, Y_coord, force ,lifted
	p = Peripheral(dev.addr, ADDR_TYPE_RANDOM).withDelegate(NotificationHandler())
	p.setMTU(515)#76

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
	print("chars:",chars,"type",type(chars))
	# enable notifications
	inchar = chars['2ba1']

	print(inchar.valHandle)

	p.writeCharacteristic(inchar.valHandle + 1, asUtf8('\x01\x00'), withResponse=True)

	outchar = chars['2ba0']

	# setup: VERSION_REQUEST
	print("Sending version message...")
	msg = make_packet(0x01, '\x00' * 16 + '\x12\x01' + '2.1.8.0'.ljust(16, '\0') + '2.12'.ljust(8, '\0'))
	send_packet(msg, outchar)
	# self.outchar.write(msg, withResponse=True)
	time.sleep(0.50)
	# setup: SETTING_INFO_REQUEST (pre-authentication)
	msg = make_packet(0x04, '')
	outchar.write(msg, withResponse=True)
	time.sleep(0.50)

	outchar.write(make_packet(0x05, '\x08\xf0\x6b\x3c\x00'), withResponse=True)
	# self.outchar.write(make_packet(0x05, '\x08\x00\x00\x00\x00\x00'), withResponse=True)
	outchar.write(make_packet(0x05, '\x05\x01'), withResponse=True)

	outchar.write(make_packet(0x05, '\x05\x00'), withResponse=True)
	outchar.write(make_packet(0x05, '\x05\x01'), withResponse=True)

	# hover mode enable
	outchar.write(make_packet(0x05, '\x06\x01'), withResponse=True)
	# setup: ONLINE_DATA_REQUEST
	outchar.write(make_packet(0x11, '\xff\xff'), withResponse=True)
	# setup: OFFLINE_NOTE_LIST_REQUEST
	# self.outchar.write(make_packet(0x21, '\xff\xff\xff\xff'), withResponse=True)
	# time.sleep(0.50)
		# setup: SETTING_INFO_REQUEST (post-authentication - real status request)
	# msg = asUtf8(make_packet(0x04, ''))
	# self.outchar.write(msg, withResponse=True)
	# time.sleep(0.50)
		# SETTING_CHANGE_REQUEST: DataTransmissionType (14) = Event (0)
	# self.outchar.write(asUtf8(make_packet(0x05, '\x0e\x00')), withResponse=True)
	# time.sleep(0.50)
	
	##beping at start
	outchar.write(make_packet(0x05, '\x05\x00'), withResponse=True)
	outchar.write(make_packet(0x05, '\x05\x01'), withResponse=True)

	return (p, outchar)

def runNeoPen(dev):
	global X_coord, Y_coord, force ,lifted
	(p, outchar) = initPen(dev)

	def generator():
		while True:
			# wait for notification from the pen, if there is a new notification, send it out as a signal 
			try:
				if (p.waitForNotifications(5.0)):
					yield (X_coord, Y_coord)
					# self.sigOut.emit(dataList)
			except BTLEDisconnectError:
				print("Pen disconnected!")
				return
	return generator


# overwrite the run method to continously receive data from the socket
def run():
	scanner = Scanner()
	while 1:
		print("Scanning...")
		devices = scanner.scan(2.0)

		generator = None

		for dev in devices:
			if isNeoPen(dev):
				print("Found available NeoPen %s, connecting..." % (dev.addr))
				generator = runNeoPen(dev)
				break
		scanner.clear()

		return generator
