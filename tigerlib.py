#-*- coding: utf8 -*-
import crc
import array
import socket

stx=0x02
ack=0x06
crcerror=0x15
ok_and_hasp_rsp=0x66
MULTIOPERATION=1
NO_MULTIOPERATION=0

address=""
port=3001

multisocket=None

def addWordInByteArray(ar,wrd,mode='LH'):
	''' mode LH -  HL - '''
	l=wrd & 0xFF
	h=(wrd & 0xFF00) >> 8
	if mode=='HL' :
		ar.append(h)
		ar.append(l)
		pass
	if mode=='LH' :
		ar.append(l)
		ar.append(h)
	pass
	
def addListInByteArray(ar,inlist):
	ar.append(inlist[0])
	addWordInByteArray(ar,inlist[1],'LH')
	addWordInByteArray(ar,inlist[2],'LH')
	addWordInByteArray(ar,inlist[3],'LH')
	ar.append(inlist[4])
	pass

def getList(src):
	ret=[]
	for l in src:
		if type(l)==str:
			ret.append(ord(l))
		else:
			ret.append(l)
	return ret
	
def opensocket():
	global multisocket
	multisocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	multisocket.connect((address,port))

def closesocket():
	global multisocket
	multisocket.close()

def getmultisocket(command):
	global multisocket
	multisocket.send(command)
	x=buffer(multisocket.recv(256))
	if ord(x[0])!=ok_and_hasp_rsp:
		if ord(x[0])==crcerror:
			raise Exception('CRC Error')
		raise NameError('Scale Error')
	ok_error=(ord(x[12]) & 0xF0) >> 4
	if ok_error==1:
		raise Exception ('File not create')
	if ok_error==2:
		raise Exception ('No free entries')
	if ok_error==3:
		raise Exception ('File corrupt')
	if ok_error==4:
		raise Exception ('Record not found')
	if ok_error==5:
		raise Exception ('Corrupt key')
	if ok_error==6:
		raise Exception ('Dublicate key')
	if ok_error==12:
		raise Exception ('Invalid input parameter')
	if ok_error==13:
		raise Exception ('Total error')
	if ok_error==14:
		raise Exception ('Unknown command')
	if ok_error==15:
		raise Exception ('Impossible')    
    	
	data_len=ord(x[7])*256+ord(x[6])
	multisocket.send(str(ack))
	return x[16:16+data_len]		
	pass
def setmultisocket(command):
	'''  запись '''
	global multisocket
	multisocket.send(command)
	x=buffer(multisocket.recv(256))
	if ord(x[0]) != ack :
		raise Exception('Scale Error')	
	pass
	
def getsocket(address,port,command):
	''' чтение '''
	s=socket.socket()
	s.connect((address,port))
	s.send(command)
	x=buffer(s.recv(256))
	if ord(x[0])!=ok_and_hasp_rsp:
		if ord(x[0])==crcerror:
			raise Exception('CRC Error')
		raise NameError('Scale Error')
	ok_error=(ord(x[12]) & 0xF0) >> 4
	if ok_error==1:
		raise Exception ('File not create')
	if ok_error==2:
		raise Exception ('No free entries')
	if ok_error==3:
		raise Exception ('File corrupt')
	if ok_error==4:
		raise Exception ('Record not found')
	if ok_error==5:
		raise Exception ('Corrupt key')
	if ok_error==6:
		raise Exception ('Dublicate key')
	if ok_error==12:
		raise Exception ('Invalid input parameter')
	if ok_error==13:
		raise Exception ('Total error')
	if ok_error==14:
		raise Exception ('Unknown command')
	if ok_error==15:
		raise Exception ('Impossible')    
    	
	data_len=ord(x[7])*256+ord(x[6])
	
	s.send(str(ack))
	s.close()
	return x[16:16+data_len]
		
def setsocket(address,port,command):
	''' запись '''
	s=socket.socket()
	s.connect((address,port))
	s.send(command)
	x=buffer(s.recv(256))
	if ord(x[0]) != ack :
		raise Exception('Scale Error')

	s.close()
	pass	

def convstr(val,lenstr):
	''' преобразовывает строку в cp866 и дополняет до размера пробелами'''
	#print len(val)
	val=val.decode('utf8').encode('cp866')
	while len(val)<lenstr:
		val=val+' '
	return val
	
def convbar(val):
	''' генерирует строку для кода 207 '''	
	while len(val)<13:
		val='0'+val
	return val

def getConfigScale_201():
	''' Конфигурация весов '''
	head2=[0x0,201,02,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[0]
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	ret_val=getsocket(address,port,head1)
	rt=[]
	#plu
	rt.append((ord(ret_val[5])*256)+ord(ret_val[4]))
	# количество групп
	rt.append(ord(ret_val[6]))
	#Уровни продаж
	rt.append(ord(ret_val[7]))
	#конфигурация 1
	lt=[]
	r=(ord(ret_val[19])*256)+ord(ret_val[18])
	for l in xrange(16):
		lt.append(r & 0x01)
		r=r >>1
		pass
	rt.append(lt)		
	#конфигурация 2
	lt=[]
	r=(ord(ret_val[21])*256)+ord(ret_val[20])
	for l in xrange(16):
		lt.append(r & 0x01)
		r=r >>1
		pass
	rt.append(lt)	
	#print rt
	return rt
	pass
	
def setConfigSclae_201():
	head2=[0x0,201,0,01,01]
	pass
#--------------------------------------		
def getConfigWrk_202(modesocket=0):
	''' Конфигурация обслуживания '''
	head2=[0x0,202,02,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[0]
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	if modesocket==0 :
		ret_val=getsocket(address,port,head1)
	else :
		ret_val=getmultisocket(head1)
	rt=[]
	#Режим 0
	rt.append(ord(ret_val[0]))
	#Количество клавиш 1
	rt.append(ord(ret_val[1]))
	#Выбор носителя 2
	rt.append((ord(ret_val[3])*256)+ord(ret_val[2]))
	#Отдел по умолчанию 3
	rt.append((ord(ret_val[5])*256)+ord(ret_val[4]))
	#TPLU 4
	rt.append(ord(ret_val[6]))
	#Конфигурация 1 5
	lt=[]
	r=(ord(ret_val[8])*256)+ord(ret_val[7])
	for l in xrange(16):
		lt.append(r & 0x01)
		r=r >>1
		pass
	rt.append(lt)	
	#конфигурация 2 6
	lt=[]
	r=(ord(ret_val[10])*256)+ord(ret_val[9])
	for l in xrange(16):
		lt.append(r & 0x01)
		r=r >>1
		pass	
	rt.append(lt)	
	#print rt
	return rt			
	pass

def setConfigWrk_202(modesocket=0):
	head2=[0x0,202,0,01,01]
	pass
#--------------------------------------	
def getSellers_204(sellernumber,modesocket=0):
	''' Продавцы '''
	head2=[0x0,204,02,00,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[]
	addWordInByteArray(head2,sellernumber,'LH')
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	if modesocket==0:
		ret_val=getsocket(address,port,head1)	
	else :
		ret_val=getmultisocket(head1)
	rt=[]
	rt.append(int(ord(ret_val[:1])))
	rt.append(unicode(str(ret_val[2:15]),'cp866'))
	return rt		
	pass

def setSellers_204(sellernumber,sellername,regkey=0,modesocket=0):
	head2=[0x0,204,00,00,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[]
	addWordInByteArray(head2,sellernumber,'LH')
	head2.extend(getList(convstr(sellername,20)))	
	head2.extend([0,0,0,0,0,0])
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	if modesocket==0:
		setsocket(address,port,head1)		
	else : 
	    setmultisocket(head1)
	pass
	
#-------------------------------------	
def getDepartments_206(departmentnumber):
	''' отделы '''
	head2=[0x0,206,02,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[]
	addWordInByteArray(head2,departmentnumber,'LH')
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	ret_val=getsocket(address,port,head1)
	rt=[]	
	#print ret_val
	pass

def setDepartments_206(departmentnumber,textdepartment,barcodenumber):
	head2=[0x0,206,0,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[]
	addWordInByteArray(head2,departmentnumber,'LH')
	head2.extend(getList(convstr(textdepartment,20)))
	addWordInByteArray(head2,0,'LH')
	addWordInByteArray(head2,barcodenumber,'LH')
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	setsocket(address,port,head1)	
	pass

#-------------------------------------
def getPLU_207(plu,modesocket=0):
	''' PLU 
	  выходные параметры 
	 plu,barcode,name,price,datasale,dategood,tare,tax,fixscale,group,numdoctext,flag
	'''
	head2=[0x0,207,02,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[]
	addWordInByteArray(head2,(plu & 0x0000FFFF),'LH')
	addWordInByteArray(head2,((plu & 0xFFFF0000)>>16),'LH')
	head2.extend(getList(convstr(' ',41)))
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	if modesocket==0:
		ret_val=getsocket(address,port,head1)
	else :
		ret_val=getmultisocket(head1)
	rt=[]
	rt.append(ord(ret_val[2])*65526+(ord(ret_val[1])*256)+ord(ret_val[0]))
	rt.append(ret_val[4:17])
	r=None
	if len(ret_val)==100:
		# двухстрочные весы
		rt.append(unicode(ret_val[17:77],'cp866'))
		price=((ord(ret_val[80])*65526)+(ord(ret_val[79])*256)+ord(ret_val[78]))/100.00
		rt.append(price)
		
		datesale=(ord(ret_val[97])*256)+ord(ret_val[96])
		rt.append(datesale)
		dategood=(ord(ret_val[95])*256)+ord(ret_val[94])
		rt.append(dategood)
		rt.append(ord(ret_val[83]))
		rt.append(ord(ret_val[82]))
		rt.append((ord(ret_val[87])*256)+ord(ret_val[86]))
		rt.append((ord(ret_val[91])*256)+ord(ret_val[90]))#group
		rt.append((ord(ret_val[99])*256)+ord(ret_val[98]))
		r=(ord(ret_val[93])*256)+ord(ret_val[92])	
	else :
		# однострочные весы
		rt.append(unicode(ret_val[17:45],'cp866'))
		price=((ord(ret_val[48])*65526)+(ord(ret_val[47])*256)+ord(ret_val[46]))/100.00
		rt.append(price)
		
		datesale=(ord(ret_val[65])*256)+ord(ret_val[64])
		rt.append(datesale)
		dategood=(ord(ret_val[63])*256)+ord(ret_val[62])
		rt.append(dategood)
		rt.append(ord(ret_val[51]))
		rt.append(ord(ret_val[50]))
		rt.append((ord(ret_val[55])*256)+ord(ret_val[54]))
		rt.append((ord(ret_val[59])*256)+ord(ret_val[58]))
		rt.append((ord(ret_val[67])*256)+ord(ret_val[66]))
		r=(ord(ret_val[61])*256)+ord(ret_val[60])
	lt=[]
	for l in xrange(16):
		lt.append(r & 0x01)
		r=r >>1
		pass
	rt.append(lt)
	#print rt
	return rt
	pass
	
def setPLU_207(plu,barcode,name_plu,price,tax,tarenum,fixscale=0,group=0,flg=0,timegod=499,timesale=499,misctext=0,modestr=1,modesocket=0):
	''' параметр modestr тип весов 1- однострочные 2 - двух строчные '''
	head2=[0x0,207,00,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[]
	addWordInByteArray(head2,(plu & 0x0000FFFF),'LH')
	addWordInByteArray(head2,((plu & 0xFFFF0000)>>16),'LH')
	head2.extend(getList(convbar(barcode)))
	if modestr==1 :
		head2.extend(getList(convstr(name_plu[:28],28)))
	else :
	    head2.extend(getList(convstr(name_plu[:60],60)))
	head2.extend([0xCC])  #
	p=int(price*100)
	addWordInByteArray(head2,(p & 0x0000FFFF),'LH')
	addWordInByteArray(head2,((p & 0xFFFF0000)>>16),'LH')	
	head2.extend([tax])
	head2.extend([tarenum])
	head2.extend([0x00,0x00])
	addWordInByteArray(head2,fixscale,'LH')
	head2.extend([0x00,0x00])
	addWordInByteArray(head2,group,'LH')
	addWordInByteArray(head2,flg,'LH')
	addWordInByteArray(head2,timegod,'LH')
	addWordInByteArray(head2,timesale,'LH')
	addWordInByteArray(head2,misctext,'LH')
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	#print head1
	if modesocket==0:
		setsocket(address,port,head1)
	else:
		setmultisocket(head1)
	pass
#------------------------------------	
def getMoreText_209(numbertext,modesocket=0):
	''' Дополнительные тексты '''
	head2=[0x0,209,02,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[]
	addWordInByteArray(head2,numbertext,'LH')
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	if modesocket==0:
		ret_val=getsocket(address,port,head1)
	else:
		ret_val=getmultisocket(head1)
	rt=[]
	rt.append(int(ord(ret_val[:1])))
	rt.append(unicode(str(ret_val[2:202]),'cp866'))
	return rt
	pass
	
def setMoreText_209(numbertext,text,modesocket=0):
	head2=[0x0,209,0,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[]
	addWordInByteArray(head2,numbertext,'LH')
	head2.extend(getList(convstr(text,200)))
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	if modesocket==0:
		setsocket(address,port,head1)	
	else :
		setmultisocket(head1)	
	#print head1    
	pass
	
def delMoreText_209 (numbertext,modesocket=0):
	'''
	  Удаляем запись 
	'''
	head2=[0x0,209,1,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[]
	addWordInByteArray(head2,numbertext,'LH')
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')	
	if modesocket==0:
		ret_val=getsocket(address,port,head1)
	else:
		ret_val=getmultisocket(head1)	
	pass
#------------------------------------

def getCommodityGroups_210(numgroup,modesocket=0):
	''' Товарные группы '''
	head2=[0x0,210,02,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[]
	addWordInByteArray(head2,numgroup,'LH')
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')	
	if modesocket==0:
		ret_val=getsocket(address,port,head1)
	else :
		ret_val=getmultisocket(head1)
	rt=[]
	rt.append(int(ord(ret_val[:1])))
	rt.append(unicode(str(ret_val[2:20]),'cp866'))
	rt.append(int(ord(ret_val[22:23])))
	return rt
	
def setCommodityGroups_210(numgroup,grouptext,rootgroup,modesocket=0):
	head2=[0x0,210,0,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[]
	addWordInByteArray(head2,numgroup,'LH')
	head2.extend(getList(convstr(grouptext,20)))
	addWordInByteArray(head2,rootgroup,'LH')	
	header.extend(head2)		
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	if modesocket==0:
		setsocket(address,port,head1)
	else :
		setmultisocket(head1)
	
	pass
#------------------------------------
def getHeaders_211(type_header):
	''' Колонтитулы '''
	head2=[0x0,211,02,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[]
	addWordInByteArray(head2,type_header,'LH')
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	ret_val=getsocket(address,port,head1)	
	rt=[]
	rt.append(int(ord(ret_val[:1])))
	rt.append(ret_val[3:4])
	rt.append(unicode(str(ret_val[4:140]),'cp866'))
	return rt	

def setHeaders_211(type_header,font_size,headerstring):

	if not (type_header in (0,1) ):
		raise 'Параметр вне диапазона'
	head2=[0x0,211,0,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[]
	addWordInByteArray(head2,type_header,'LH')
	head2.extend([0x05])
	head2.extend([ord(font_size)])
	head2.extend(getList(convstr(headerstring,140)))
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')	
	setsocket(address,port,head1)
	
#------------------------------------
def getOrganisation_212():
	''' Организация '''
	head2=[0x0,212,02,00,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[0x01,0x00]
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	ret_val=getsocket(address,port,head1)
	rt=[]
	rt.append(int(ord(ret_val[:1])))
	rt.append(unicode(str(ret_val[2:60]),'cp866'))
	return rt	
	pass
def setOrganisation_212(nameorganisation):
	head2=[0x0,212,0,00,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[0x01,0x00]
	head2.extend(getList(convstr(nameorganisation,70)))
	header.extend(head2)	
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	setsocket(address,port,head1)
	pass	
	
#-----------------------------------
def getScrollString_213():
	''' Бегущая строка '''
	# возможно нет ответной функции проверить
	head2=[0x0,213,02,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head1.append(stx)
	addWordInByteArray(head1,8,'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,0,'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	#print head1
	ret_val=getsocket(address,port,head1)
	
	pass
def setScrollString_213(scrollstring):
	head2=[0x0,213,0,01,01]
	head1=array.array('B')
	header=array.array('B')
	head2.extend(getList(convstr(scrollstring,100)))
	addListInByteArray(header,head2)
	head2=[]
	head2.extend(getList(convstr(scrollstring,100)))
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	setsocket(address,port,head1)	
	pass
#-----------------------------------	
def getBarCode_214(numberbarcode,modesocket=0):
	''' Настройка штрихкодов чтение'''
	if (numberbarcode<1 or numberbarcode>32) : raise Exception('Value out range')
	head2=[0x00,214,02,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	header.append(numberbarcode)    # номер штрихкода
	head1.append(stx)
	addWordInByteArray(head1,9,'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,1,'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	if modesocket==0:
		ret_val=getsocket(address,port,head1)
	else :
		ret_val=getmultisocket(head1)
	rt=[]
	rt.append(int(ord(ret_val[:1])))
	rt.append(str(ret_val[2:15]))
	return rt

def setBarCode_214(numberbarcode,maskbarcode,modesocket=0):
	''' Настройка штрихкодов запись '''
	if (numberbarcode<1 or numberbarcode>32) : raise Exception('Value out range')	
	#maskbarcode - 13 
	head2=[0x0,214,0x0,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[numberbarcode,0x30]
	head2.extend(getList(maskbarcode))
	head2.extend([0x20,0x20,0x20,0x20,0x20])
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	if modesocket==0:
		setsocket(address,port,head1)
	else :
		setmultisocket(head1)
	pass

#------------------------------------

def getTara_215(numbertare):
	''' Тара '''
	if (numbertare<1 or numbertare>16) : raise Exception('Value out range')
	head2=[0x0,215,02,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	
	addWordInByteArray(header,numbertare,'LH')
	
	head1.append(stx)
	addWordInByteArray(head1,10,'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,2,'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	ret_val=getsocket(address,port,head1)
	pass
	
def setTara_215(numbertare,weight):
	''' Тара установка '''
	if (numbertare<1 or numbertare>16) : raise Exception('Value out range')
	head2=[0x0,215,0,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[]
	addWordInByteArray(head2,numbertare,'LH')
	addWordInByteArray(head2,(weight & 0x0000FFFF),'LH')
	addWordInByteArray(head2,((weight & 0xFFFF0000)>>16),'LH')
	#hh=(wight & 0xFFFF0000)>>16
	#ll=(wight & 0x0000FFFF)
	header.extend(head2)
	head1.append(stx)                                 # 
	addWordInByteArray(head1,8+1*len(head2),'LH')     # ---------------
	addWordInByteArray(head1,1,'LH')                  # расчет размеров и длинн тела 
	addWordInByteArray(head1,len(head2),'LH')         # ----------------
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')
	
	setsocket(address,port,head1)
	pass
	
#-----------------------------------
def getFixKey_216(numberkey,modesocket=0):
	''' Фиксированные клавиши '''
	if (numberkey<1 or numberkey>109) : raise Exception('Value out range')
	head2=[0x0,216,2,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	addWordInByteArray(header,numberkey,'LH')
	
	head1.append(stx)
	addWordInByteArray(head1,10,'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,2,'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')	
	if modesocket==0:
		ret_val=getsocket(address,port,head1)
	else :
		ret_val=getmultisocket(head1)		

	rt=[]
	rt.append((ord(ret_val[1])*256)+ord(ret_val[0]))
	rt.append((ord(ret_val[3])*256)+ord(ret_val[2]))
	rt.append((ord(ret_val[6])*65526)+(ord(ret_val[5])*256)+ord(ret_val[4]))

	#print rt
	return rt

def setFixKey_216(numberkey,numberretail,numberplu,modesocket=0):
	if (numberkey<1 or numberkey>109) : raise Exception('Value out range')
	head2=[0x0,216,0,01,01]
	head1=array.array('B')
	header=array.array('B')
	addListInByteArray(header,head2)
	head2=[]
	addWordInByteArray(head2,numberkey,'LH')
	addWordInByteArray(head2,numberretail,'LH')
	#  4 байта номера plu
	addWordInByteArray(head2,(numberplu & 0x0000FFFF),'LH')
	addWordInByteArray(head2,((numberplu & 0xFFFF0000)>>16),'LH')
	head2.extend([0x00,0x00,0x00,0x00,0x00,0x00])
	header.extend(head2)
	head1.append(stx)
	addWordInByteArray(head1,8+1*len(head2),'LH')
	addWordInByteArray(head1,1,'LH')
	addWordInByteArray(head1,len(head2),'LH')
	head1.extend(header)
	addWordInByteArray(head1,crc.crc16(head1.tostring()[1:],crc.CRC_CCITT_XMODEM),'HL')	
	if modesocket==0:
		setsocket(address,port,head1)
	else :
		setmultisocket(head1)	

	pass 
#---------------------------------------
def getReclamaText_220(numberkey):
	pass
def setReclamaText_220(numberkey,reclamatext):
	pass


