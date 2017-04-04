#!/usr/bin/python -O
#-*- coding: utf-8 -*-
#
'''
   (c) CAV Inc
   
'''

import pygtk
pygtk.require('2.0')
import gtk,os
import glu
import workfrm
import labeldesign
import setkeyplu

class App():
	win_list=[]
	def __destroy(self,widget):
		glu.SaveCFG(glu.getKey('USER PATH')+os.sep+'.metler_scale'+os.sep+'tiger.ini')
		gtk.main_quit()
		return False
	
	def __on_click(self,widget,data=None):
		if data=='quit':
			self.__destroy(widget)
		if data=='setlink':
			if len(self.win_list)>0:
				self.hbox.remove(self.win_list.pop())
			sl=workfrm.SetScaleLink()
			self.win_list.append(sl)
			self.hbox.pack_start(sl,True,True)
		if data=='barcodemask':
			if len(self.win_list)>0:
				self.hbox.remove(self.win_list.pop())
			sl=workfrm.SetBarMask()
			self.win_list.append(sl)
			self.hbox.pack_start(sl,True,True)
		if data=='scrollstr':
			if len(self.win_list)>0:
				self.hbox.remove(self.win_list.pop())
			sl=workfrm.SetScrollString()
			self.win_list.append(sl)
			self.hbox.pack_start(sl,True,True)
		if data=='colontituls':
			if len(self.win_list)>0:
				self.hbox.remove(self.win_list.pop())
			sl=workfrm.Colontitul()
			self.win_list.append(sl)
			self.hbox.pack_start(sl,True,True)	
		if data=='shopname':
			if len(self.win_list)>0:
				self.hbox.remove(self.win_list.pop())
			sl=workfrm.SetShopName()
			self.win_list.append(sl)
			self.hbox.pack_start(sl,True,True)
		if data=='misktext':
			if len(self.win_list)>0:
				self.hbox.remove(self.win_list.pop())
			sl=workfrm.SetReclamText()
			self.win_list.append(sl)
			self.hbox.pack_start(sl,True,True)
		if data=='doptext':
			if len(self.win_list)>0:
				self.hbox.remove(self.win_list.pop())
			sl=workfrm.SetDocText()
			self.win_list.append(sl)
			self.hbox.pack_start(sl,True,True)
			pass
		if data=='tare':
			if len(self.win_list)>0:
				self.hbox.remove(self.win_list.pop())
			sl=workfrm.SetTare()
			self.win_list.append(sl)
			self.hbox.pack_start(sl,True,True)
			pass
		if data=='plu':
			if len(self.win_list)>0:
				self.hbox.remove(self.win_list.pop())
			sl=workfrm.SetPlu()
			self.win_list.append(sl)
			self.hbox.pack_start(sl,True,True)
		if data=='selers':
			if len(self.win_list)>0:
				self.hbox.remove(self.win_list.pop())
			sl=workfrm.SetPerson()
			self.win_list.append(sl)
			self.hbox.pack_start(sl,True,True)
		if data=='grouptovar':
			if len(self.win_list)>0:
				self.hbox.remove(self.win_list.pop())
			sl=workfrm.SetGroup()
			self.win_list.append(sl)
			self.hbox.pack_start(sl,True,True)
		if data=='configsale':
			if len(self.win_list)>0:
				self.hbox.remove(self.win_list.pop())
			sl=workfrm.SetConfScale()
			self.win_list.append(sl)
			self.hbox.pack_start(sl,True,True)
		if data=='labeldesign':
			if len(self.win_list)>0:
				self.hbox.remove(self.win_list.pop())
			sl=labeldesign.LabelDesign()
			self.win_list.append(sl)
			self.hbox.pack_start(sl,True,True)
		if data=='setkeyplu':
			if len(glu.pludata)==0:
				dialog=gtk.Dialog("Внимание !!!!",None,
				gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,(gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
				lb=gtk.Label('  Не загружен список товаров !  ')
				dialog.vbox.pack_start(lb,False,True)
				lb.show()
				response = dialog.run()
				dialog.destroy()
				return
				pass
				
			if len(self.win_list)>0:
				self.hbox.remove(self.win_list.pop())
			sl=setkeyplu.SetKeyInPlu()
			self.win_list.append(sl)
			self.hbox.pack_start(sl,True,True)
			
		if data=='about':
			self.about_dialog()
		pass
			
	def about_dialog(self):
		about=gtk.AboutDialog()
		about.set_program_name('Работа с весами Metler Toledo Tiger P')
		about.set_version('1.0')
		about.set_copyright('(c) CAV Inc')
		about.set_license('LGPL')
		
		about.run()
		about.destroy()
		
		
	def __set_menu_main(self,title,submenu=None):
		m_item=gtk.MenuItem(title)
		if submenu!=None:
			menu=gtk.Menu()
			for l in submenu:
				if l=='-':
					item=gtk.SeparatorMenuItem()
				else:
					if len(l)!=2:
						item=gtk.MenuItem(l)
					else:
						item=gtk.MenuItem(l[0])
						item.connect_object("activate",self.__on_click,l[1],l[1])
				menu.append(item)
			m_item.set_submenu(menu)
		return m_item		
		
	def __set_menu(self):
		mb=gtk.MenuBar()
		mb.add(self.__set_menu_main('Весы',[[u'Настрока подключения','setlink'],[u'Выход','quit']]))
		mb.add(self.__set_menu_main('Данные',[['Товары','plu'],'-',[u'Группы товаров','grouptovar'],[u'Продавцы','selers'],[u'Тара','tare'],'-',[u'Маска штрихкода','barcodemask'],'-',[u'Бегущая строка','scrollstr'],[u'Верхний и нижний текст чека','colontituls'],[u'Название магазина','shopname'],[u'Рекламный текст','misktext'],[u'Дополнительные тексты(ингридиенты)','doptext']]))
		mb.add(self.__set_menu_main('Конфигурация',[['Конфигурация обслуживания','configsale']]))
		mb.add(self.__set_menu_main('Редактор этикеток',[[u'Редактор этикеток','labeldesign'],[u'Редактор клавиатуры PLU','setkeyplu']]))
		mb.add(self.__set_menu_main('Помощь',[[u'О программе','about']]))
		return mb
	
	def set_message_sb(self,msg):
		context_id=self.sb.get_context_id('')
		self.sb.push(msg,context_id)
				
	def __init__(self):
		win = gtk.Window(gtk.WINDOW_TOPLEVEL)
		win.set_title('Работа с весами Metler Toledo Tiger')
		win.set_default_size(win.get_screen().get_width(),400)
		win.connect('destroy',self.__destroy)
		win.set_icon_from_file('scales.png')
		vbox=gtk.VBox()
		vbox.pack_start(self.__set_menu(),False,True,4)
		self.hbox=gtk.HBox()
		vbox.pack_start(self.hbox,True,True,4)
		self.sb=gtk.Statusbar()
		vbox.pack_start(self.sb,False,True,4)
		win.add(vbox)
		win.show_all()
		
		
	def main(self):
		gtk.main()
		pass

if __name__=='__main__':
	glu.TestAndDefaultGreate()
	glu.LoadCFG(glu.getKey('USER PATH')+os.sep+'.metler_scale'+os.sep+'tiger.ini')
	App().main()
