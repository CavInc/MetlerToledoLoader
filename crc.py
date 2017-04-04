#-*- coding: UTF-8 -*-
# LGPL 2011.06 Kotov Alexander
#
# thanks:   Lammert Bies  http://www.lammertbies.nl/comm/info/crc-calculation.html
#
'''
   caclculate CRC16
     constant:  CRC16
                CRC16_MODBUS
                CRC16_CCITT (0xFFFF)
                CRC16_CCITT_x1D0F (0x1D0F)
                CRC_CCITT_XMODEM
                
'''
__author__='Kotov Alaxander'

CRC16=0
CRC16_CCITT=1
CRC_CCITT_XMODEM=2
CRC16_CCITT_x1D0F=3
CRC16_MODBUS=4

def crc16(buffer,mode=CRC16_CCITT):
	if mode==CRC16_CCITT:
		polynom=0x1021
		crc16ret=0xFFFF
		
	if mode==CRC16_CCITT_x1D0F:
		polynom=0x1021
		crc16ret=0x1D0F
			
	if mode==CRC_CCITT_XMODEM:
		polynom=0x1021
		crc16ret=0
		
	if mode==CRC16:
		polynom=0xA001 #0x8005
		crc16ret=0 # 0xFFFF 
	
	if mode==CRC16_MODBUS:
		polynom=0xA001
		crc16ret=0xFFFF
   		
		
	if (mode!=CRC16) and (mode!=CRC16_MODBUS):
		for l in buffer:
			crc16ret ^=ord(l) << 8
			crc16ret &=0xFFFF
			for i in xrange(0,8):
				if (crc16ret & 0x8000):
					crc16ret=(crc16ret << 1) ^ polynom
				else :
					crc16ret=crc16ret << 1
				crc16ret &=0xFFFF
	else :
		for l in buffer:
			crc16ret ^=ord(l) 
			crc16ret &=0xFFFF
			for i in xrange(8):
				if (crc16ret & 0x0001):
					crc16ret=(crc16ret >> 1) ^ polynom
				else :
					crc16ret=crc16ret >> 1
				crc16ret &=0xFFFF	
		
	return crc16ret
