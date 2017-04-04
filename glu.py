#-*- coding:utf-8 -*-
''' 
    (c) CAV Inc
    Работа с конфигурацией и параметрами
    параметры сохраняются в каталоге пользователя
'''
import os
import ConfigParser

prop={}
pludata=[]
keyplulink={}

def TestAndGreateDir(foldername):
	''' проверяет и создает при остутствии каталог '''
	if os.access(foldername,os.F_OK)!=True :
		os.mkdir(foldername)
		return True
	return False

def TestAndDefaultGreate():
	global prop
	user_path=os.path.expanduser('~')
	prop['USER PATH']=user_path
	prop['Count Scale']=0
	if TestAndGreateDir(user_path+os.sep+'.metler_scale'):
		SaveCFG(user_path+os.sep+'.metler_scale'+os.sep+'tiger.ini')
		pass
		
	
def getKey(key):
	global prop
	return prop[key]
	
def setKey(key,val):
	global prop
	prop[key]=val
def testKey(key):
	global prop
	return prop.has_key(key)
def delKey(key):
	global prop
	del prop[key]	


def LoadCFG(inifile):
	cp=ConfigParser.ConfigParser()
	cp.read(inifile)
	setKey('Count Scale',int(cp.get('scale','Count Scale')))
	for i in xrange(getKey('Count Scale')):
		setKey('Num '+str(i+1),cp.get('scale','Num '+str(i+1)))
		setKey('Name Scale '+str(i+1),cp.get('scale','Name Scale '+str(i+1)))
		setKey('IP '+str(i+1),cp.get('scale','IP '+str(i+1)))
		setKey('Scale use '+str(i+1),bool(cp.get('scale','Scale use '+str(i+1))))
		if cp.has_option('scale','Number Line '+str(i+1)):
			setKey('Number line '+str(i+1),cp.get('scale','Number Line '+str(i+1)))
		else :
			setKey('Number line '+str(i+1),1)
	
	for i in xrange(1,9):
		if cp.has_option('barmask','BarMask Num '+str(i)):
			setKey('BarMask Num '+str(i),int(cp.get('barmask','BarMask Num '+str(i))))
			setKey('BarMask '+str(i),cp.get('barmask','BarMask '+str(i)))
			
	if cp.has_option('barmask','BarMask count') :
		setKey('BarMask count',int(cp.get('barmask','BarMask count')))
		
	for i in xrange(1,2000):
		if cp.has_option('ingridient','Dop Text '+str(i)):
			setKey('Dop Text '+str(i),cp.get('ingridient','Dop Text '+str(i)))
			setKey('Dop Num '+str(i),cp.get('ingridient','Dop Num '+str(i)))
	
	for i in xrange(1,99):
		if cp.has_option('selers','Pers Num '+str(i)):
			setKey('Pers Num '+str(i),cp.get('selers','Pers Num '+str(i)))
			setKey('Pers Text '+str(i),cp.get('selers','Pers Text '+str(i)))	
		
	for i in xrange(1,20):
		if cp.has_option('group','Group Text '+str(i)):
			setKey('Group Num '+str(i),cp.get('group','Group Num '+str(i)))
			setKey('Group Text '+str(i),cp.get('group','Group Text '+str(i)))
	#print prop
	pass

def SaveCFG(inifile):
	cp=ConfigParser.ConfigParser()
	cp.add_section('scale')
	cp.set('scale','Count Scale',getKey('Count Scale'))
	for i in xrange(getKey('Count Scale')):
		cp.set('scale','Num '+str(i+1),getKey('Num '+str(i+1)))
		cp.set('scale','Name Scale '+str(i+1),getKey('Name Scale '+str(i+1)))
		cp.set('scale','IP '+str(i+1),getKey('IP '+str(i+1)))
		cp.set('scale','Scale use '+str(i+1),getKey('Scale use '+str(i+1)))
		cp.set('scale','Number Line '+str(i+1),getKey('Number line '+str(i+1)))
		pass
	
	cp.add_section('barmask')
	for i in xrange(1,9):
		if prop.has_key('BarMask Num '+str(i)):
			cp.set('barmask','BarMask Num '+str(i),getKey('BarMask Num '+str(i)))
			cp.set('barmask','BarMask '+str(i),getKey('BarMask '+str(i)))
			
	cp.add_section('ingridient')		
	for i in xrange(1,2000):
		if prop.has_key('Dop Text '+str(i)):
			cp.set('ingridient','Dop Num '+str(i),getKey('Dop Num '+str(i)))
			cp.set('ingridient','Dop Text '+str(i),getKey('Dop Text '+str(i)))
			pass
		pass
		
	cp.add_section('selers')
	for i in xrange(1,99):
		if prop.has_key('Pers Text '+str(i)):
			cp.set('selers','Pers Num '+str(i),getKey('Pers Num '+str(i)))
			cp.set('selers','Pers Text '+str(i),getKey('Pers Text '+str(i)))
			
	cp.add_section('group')
	for i in xrange(1,20):
		if prop.has_key('Group Text '+str(i)):
			cp.set('group','Group Num '+str(i),getKey('Group Num '+str(i)))
			cp.set('group','Group Text '+str(i),getKey('Group Text '+str(i)))

	cp.write(open(inifile,'w'))
	pass
