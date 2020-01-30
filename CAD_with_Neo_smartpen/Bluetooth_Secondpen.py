from __future__ import print_function
from bluepy.btle import *
#import bluepy.btle
import struct
import time
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Queue import Queue

X_coord = 0
Y_coord = 0
force = 0

	
def isNeoPen(dev):
	for adtype, desc, value in dev.getScanData():
		if desc == 'Manufacturer' and value == u'9c7bd202f82a':
			return True
	return False
	



class NotificationHandler(DefaultDelegate):
	def __init__(self, msgq):
		DefaultDelegate.__init__(self)
		self.msgq = msgq

	def handleNotification(self, cHandle, data):
		#print("Notification: 0x%04x %s" % (cHandle,data.encode('hex')))
		self.msgq.put((cHandle, data))
		

def shortUUID(s):
	assert len(s) == 4
	return '0000' + s.lower() + '-0000-1000-8000-00805f9b34fb'

def getCharacteristics(svc):
	return {str(c.uuid): c for c in svc.getCharacteristics()}			
		
class BluetoothThread(QThread):	
	sigOut = pyqtSignal(list)
	def Dot_Decod(self, msg):
		global X_coord, Y_coord, force
		x=(int(msg[4:6],16))*100+(int(msg[12:14],16)) # X coordinate +fx
		y=(int(msg[8:10],16))*100+(int(msg[14:16],16)) # Y coordinate +fy
		force=((int(msg[16:18],16))) # pressure
		X_coord = .175*x/4.375
		Y_coord = .175*y/4.375
		force = force
			# print("x:%i y:%i force: %i" % (x/4.375,y/4.375,force))		
	def runNeoPen(self, dev):
		global X_coord, Y_coord, force
		lifted=False
		msgq = Queue()
		p = Peripheral(dev.addr, ADDR_TYPE_PUBLIC).withDelegate(NotificationHandler(msgq))
		p.setMTU(44)
		svcs = {str(s.uuid) : s for s in p.getServices()}

		for uuid in ('1800', '180a'):
			svc = svcs.get(shortUUID(uuid), None)
			if svc is None:
				continue
			print(svc.uuid.getCommonName())
			for char in svc.getCharacteristics():
				print("  %s = %s" % (char.uuid.getCommonName(), char.read()))

		system2_svc = svcs[shortUUID('18f6')]
		system_svc = svcs[shortUUID('18f5')]
		pen_svc = svcs[shortUUID('18f1')]
		system2_chars = getCharacteristics(system2_svc)
		system_chars = getCharacteristics(system_svc)
		pen_chars = getCharacteristics(pen_svc)

		set_note_id_list_char = system_chars[shortUUID('2ab2')]
		# XXX hardcoded
		note_id_list = '02071b0000031b0000001b00000e590200045a0200045b0200045d020004000100d605020100000029610e000100'.decode('hex')
		set_note_id_list_char.write(note_id_list, withResponse=True)

		print("Subscribing to pen notifications")
		notif = {}
		# enable notifications on *everything*
		for svc_id, char_ids in [
			('18f1', ('2aa0', '2aa1', '2aa2')),
			('18f2', ('2ac2',)),
			('18f3', ('2ac8', '2ac9', '2aca', '2acc')),
			('18f4', ('2ad2', '2ad4')),
			('18f5', ('2ab0', '2ab5')),
			('18f6', ('2ab7', '2aba')),
		]:
			svc = svcs[shortUUID(svc_id)]
			chars = getCharacteristics(svc)
			for char_id in char_ids:
				handle = chars[shortUUID(char_id)].valHandle
				notif[handle] = (svc_id, char_id)
				p.writeCharacteristic(handle + 1, '\x01\x00', withResponse=True)

		init_pen_state = True
		while True:
			p.waitForNotifications(1.0)

			while not msgq.empty():
				msgh, msg = msgq.get()
				svc_id, char_id = notif[msgh]
				#print(svc_id, char_id, msg.encode('hex'))
				if (svc_id, char_id) == ('18f5', '2ab5'):
					# READY_EXCHANGE_DATA_REQUEST
					ready_exchange_char = system_chars[shortUUID('2ab4')]
					ready_exchange_char.write('\x01', withResponse=True)
				elif (svc_id, char_id) == ('18f6', '2ab7'):
					# PEN_PASSWORD_REQUEST
					self.pw_response_char = system2_chars[shortUUID('2ab8')]
					self.pw_response_char.write('0000' + '\x00' * 12, withResponse=True)
				elif (svc_id, char_id) == ('18f5', '2ab0') and init_pen_state:
					init_pen_state = False

					_version, _penStatus, _timezoneOffset, _timeTick, \
						_pressureMax, _battLevel, _memoryUsed,\
						_colorState, _usePenTipOnOff, _useAccelerator, \
						_useHover, _beepOnOff, _autoPwrOffTime, _penPressure \
						= struct.unpack('<BBiQBBBIBBBBHH11x', msg)
					_timeTick += 500 # ms, fakery
					_colorState = 1 # ???
					_useHover = 0
					newmsg = struct.pack('<iQIBBBBHH16x', _timezoneOffset, _timeTick, \
						_colorState, _usePenTipOnOff, _useAccelerator, \
						_useHover, _beepOnOff, _autoPwrOffTime, _penPressure)
						
					set_pen_state_char = system_chars[shortUUID('2ab1')]
					set_pen_state_char.write(newmsg, withResponse=True)
				elif (svc_id, char_id) == ('18f1', '2aa1'):
					_owner, _note, _page = struct.unpack('<III', msg)
					print('Note ID changed:', _owner, _note, _page)
					
					
				elif (svc_id, char_id) == ('18f1', '2aa0'):
					pen_Msg=msg.encode('hex')
					self.Dot_Decod(pen_Msg)
					dataList = [X_coord, Y_coord, force, lifted]
					self.sigOut.emit(dataList)
				
				
				elif (svc_id, char_id) == ('18f1', '2aa2'):
					pen_Msg=msg.encode('hex')
					#lifted=pen_Msg
					#self.Dot_Decod(pen_Msg)
					if(pen_Msg[-9] == '1'):
						lifted=True
						force=0
					elif (pen_Msg[-9] == '0'):
						lifted=False
					dataList = [X_coord, Y_coord, force, lifted]
					self.sigOut.emit(dataList)
	def beep(self):
		self.pw_response_char.write('0000' + '\x00' * 12, withResponse=True) # creating the beep sound

						
		

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


