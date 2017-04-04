#-*- coding: utf-8 -*-
import gtk
import glu
import tigerlib
import time,csv
import sysfrm
import pickle
import os

class SetScaleLink(gtk.Frame):
	''' настройки списка весов'''
	def __on_click(self,widget,data=None):
		if data=='insert':
			iefrm=InsEditScale(0)
			iefrm.run()
			if iefrm.ok:
				i=int(glu.getKey('Count Scale'))
				i+=1
				glu.setKey('Num '+str(i),i)
				glu.setKey('Name Scale '+str(i),iefrm.nameScale.get_text())
				glu.setKey('IP '+str(i),iefrm.ipAdress.get_text())
				glu.setKey('Scale use '+str(i),True)
				glu.setKey('Count Scale',i)
				glu.setKey('Number line '+str(i),iefrm.lineNum.get_text())
			iefrm.destroy()
			#print glu.prop
			self.__refresh()
			
		if data=='edit':
			if self.sel_id==None:
				return True
			iefrm=InsEditScale(1,glu.getKey('Name Scale '+str(self.sel_id)),glu.getKey('IP '+str(self.sel_id)),glu.getKey('Number line '+str(self.sel_id)))
			iefrm.run()
			if iefrm.ok:
				glu.setKey('Num '+str(self.sel_id),self.sel_id)
				glu.setKey('Name Scale '+str(self.sel_id),iefrm.nameScale.get_text())
				glu.setKey('IP '+str(self.sel_id),iefrm.ipAdress.get_text())	
				glu.setKey('Number line '+str(self.sel_id),iefrm.lineNum.get_text())
			iefrm.destroy()	
			self.__refresh()
		if data=='del':
			# TODO удаление не работает
			glu.delKey('Num '+str(self.sel_id))
			glu.delKey('Name Scale '+str(self.sel_id))
			glu.delKey('IP '+str(self.sel_id))
			glu.delKey('Number line '+str(self.sel_id))
			self.__refresh()
			pass
		pass
	
	def __on_row_selected(self,widget):
		tree_model,tree_iter=widget.get_selection().get_selected()
		if tree_iter!=None:
			self.sel_id=tree_model.get_value(tree_iter,0)
		pass		
	
	def __get_separator(self):
		sep=gtk.SeparatorToolItem()
		return sep	
	def __set_toolbar(self):
		tb=gtk.Toolbar()
		tb.set_style(gtk.TOOLBAR_ICONS)
		insbutton=gtk.ToolButton(gtk.STOCK_NEW)
		insbutton.connect('clicked',self.__on_click,'insert')
		tb.insert(insbutton,0)
		editbutton=gtk.ToolButton(gtk.STOCK_EDIT)
		editbutton.connect('clicked',self.__on_click,'edit')
		tb.insert(editbutton,1)
		tb.insert(self.__get_separator(),2)
		delbutton=gtk.ToolButton(gtk.STOCK_DELETE)
		delbutton.connect('clicked',self.__on_click,'del')
		delbutton.set_tooltip_text('Удалить запись')
		tb.insert(delbutton,3)
		
		return tb
		
	def __set_model(self):
		self.lst=gtk.ListStore(int,str,str,'gboolean',int)
		self.__refresh()
		return self.lst
		
	def __refresh(self):
		self.lst.clear()
		for i in xrange(glu.getKey('Count Scale')):
			#print type(glu.getKey('Scale use '+str(i+1)))
			self.lst.append([int(glu.getKey('Num '+str(i+1))),glu.getKey('Name Scale '+str(i+1)),glu.getKey('IP '+str(i+1)),glu.getKey('Scale use '+str(i+1)),int(glu.getKey('Number line '+str(i+1)))])
	
	def __set_columns(self,tree):
		renderText=gtk.CellRendererText()
		column=gtk.TreeViewColumn('#',renderText,text=0)
		tree.append_column(column)
		column=gtk.TreeViewColumn('Наименование',renderText,text=1)
		tree.append_column(column)
		column=gtk.TreeViewColumn('IP Адрес',renderText,text=2)
		#column.set_tooltip_text('IP Адрес весов')
		tree.append_column(column)
		renderBool=gtk.CellRendererToggle()
		column=gtk.TreeViewColumn('...',renderBool)
		#column=gtk.TreeViewColumn('...',renderText,text=3)
		tree.append_column(column)
		column=gtk.TreeViewColumn('Кол.-во строк',renderText,text=4)
		tree.append_column(column)
			
	def __init__(self):
		gtk.Frame.__init__(self)
		self.set_label('Список весов')
		vbox=gtk.VBox()
		vbox.pack_start(self.__set_toolbar(),False,True,3)
		sw=gtk.ScrolledWindow()
		table=gtk.TreeView(self.__set_model())
		table.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
		table.set_rules_hint(True)
		table.connect('cursor-changed',self.__on_row_selected)
		self.__set_columns(table)
		sw.add(table)
		sw.show_all()
		vbox.pack_start(sw,True,True,0)
		self.add(vbox)
		self.show_all()
		pass

class InsEditScale(gtk.Dialog):
	def __on_close(self,widget,data=None):
		self.response(gtk.RESPONSE_CLOSE)
		pass
	def __on_click(self,widget,data=None):
		if data=='run':
			self.ok=True
			self.__on_close(widget)
		pass
			
	def __init__(self,mode,nameS=None,ipAd=None,lineNumber=1):
		super(InsEditScale,self).__init__()
		self.ok=False

		lb1=gtk.Label('Название весов')
		lb1.set_justify(gtk.JUSTIFY_LEFT)
		self.nameScale=gtk.Entry()
		self.vbox.pack_start(lb1,False,True,0)
		self.vbox.pack_start(self.nameScale,False,True,4)
		lb2=gtk.Label('IP Адес весов')
		self.ipAdress=gtk.Entry()
		self.vbox.pack_start(lb2,False,True,0)
		self.vbox.pack_start(self.ipAdress,False,True,4)	
		self.vbox.pack_start(gtk.Label('Версия прошивки весов (одно или двух строчная)'),False,True,0)	
		self.lineNum=gtk.Entry(1)
		self.vbox.pack_start(self.lineNum,False,True,4)
		if mode==0 :
			self.set_title('Добавить')
			self.lineNum.set_text(str(lineNumber))
		else :
			self.set_title('Редактировать')
			self.nameScale.set_text(nameS)
			self.ipAdress.set_text(ipAd)
			self.lineNum.set_text(lineNumber)
			
						
		bt1=gtk.Button('Принять')
		bt1.connect('clicked',self.__on_click,'run')
		bt2=gtk.Button('Закрыть')
		bt2.connect('clicked',self.__on_close)
		self.action_area.pack_start(bt1,False,True,4)
		self.action_area.pack_start(bt2,False,True,4)		
		
		self.show_all()
		
class SetBarMask(gtk.Frame):
	''' маска штрих кода  '''
	def __clear_bar(self):
		for i in xrange(1,9):
			if glu.testKey('BarMask Num '+str(i)):
				glu.delKey('BarMask Num '+str(i))
				glu.delKey('BarMask '+str(i))
		pass
		
	def __on_click(self,widget,data=None):
		if data=='new':
			if len(self.num.get_text())!=0 :
				i=0
				if int(self.num.get_text())>8: return None
				ii=int(self.num.get_text())
				if glu.testKey('BarMask count'):
					i=glu.getKey('BarMask count')
				glu.setKey('BarMask Num '+str(ii),int(self.num.get_text()))
				glu.setKey('BarMask '+str(ii),self.mes.get_text())
				i +=1
				glu.setKey('BarMask count',i)
				self.__refresh()
				pass
			pass
		if data=='del':
			glu.delKey('BarMask Num '+str(self.sel_id))
			glu.delKey('BarMask '+str(self.sel_id))
			self.__refresh()
			pass
		if data=='sendcale':
			selscale=sysfrm.SelectScale()
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False
			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						tigerlib.opensocket()
						for i in xrange(1,9):
							tigerlib.setBarCode_214(i,glu.getKey('BarMask '+str(i)),tigerlib.MULTIOPERATION)
							#time.sleep(1)
						pass
						tigerlib.closesocket()
			pass
			
		if data=='resivescale':
			selscale=sysfrm.SelectScale(1)
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False	
			
			self.__clear_bar()
			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						#print tigerlib.address
						tigerlib.opensocket()
						for i in xrange(1,9):
							num,st=tigerlib.getBarCode_214(i,tigerlib.MULTIOPERATION)
							glu.setKey('BarMask Num '+str(i),num)
							glu.setKey('BarMask '+str(i),st)
							#time.sleep(1)
						tigerlib.closesocket()
						self.__refresh()
		pass
	
	def __on_row_selected(self,widget):
		tree_model,tree_iter=widget.get_selection().get_selected()
		if tree_iter!=None:
			self.sel_id=tree_model.get_value(tree_iter,0)
			pass
	def __on_row_activated(self,widget,row,col):
		tree_model,tree_iter=widget.get_selection().get_selected()
		if tree_iter!=None:
			id=tree_model.get_value(tree_iter,0)
			if glu.testKey('BarMask Num '+str(id)):
				self.num.set_text(str(glu.getKey('BarMask Num '+str(id))))
				self.mes.set_text(glu.getKey('BarMask '+str(id)))
		
			
	def __refresh(self):
		self.lstbar.clear()
		for i in xrange(1,9):
			if glu.testKey('BarMask Num '+str(i)):
				self.lstbar.append([glu.getKey('BarMask Num '+str(i)),glu.getKey('BarMask '+str(i))])

	
	def __set_tree(self):
		self.lstbar=gtk.ListStore(int,str)
		tree=gtk.TreeView(self.lstbar)
		tree.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
		tree.connect('cursor-changed',self.__on_row_selected)
		tree.connect('row-activated',self.__on_row_activated)
		renderText=gtk.CellRendererText()
		column=gtk.TreeViewColumn('#',renderText,text=0)
		tree.append_column(column)
		column=gtk.TreeViewColumn('Маска штрихкода',renderText,text=1)
		tree.append_column(column)		
		self.__refresh()
		return tree
		
	def __dwn_lf_panel(self):
		dp=gtk.HBox()
		self.num=gtk.Entry(2)
		self.mes=gtk.Entry(13)
		dp.pack_start(self.num,False,False,4)
		dp.pack_start(self.mes,True,True,4)
		bt1=gtk.Button('Добавить')
		bt1.connect('clicked',self.__on_click,'new')
		bt2=gtk.Button('Удалить')
		bt2.connect('clicked',self.__on_click,'del')
		#bt2.unset_flags(gtk.SENSITIVE)
		#print bt2.flags()
		dp.pack_start(bt1,False,True,4)
		dp.pack_start(bt2,False,True,4)
		return dp
	def __init__(self):
		gtk.Frame.__init__(self)
		self.set_label('Настройка маски штрихкода')
		hbox=gtk.HBox()
		lfbox=gtk.VBox()
		lfbox.pack_start(self.__set_tree(),True,True,4)
		lfbox.pack_start(self.__dwn_lf_panel(),False,True,4)
		hbox.pack_start(lfbox,True,True,4)
		rfbox=gtk.VButtonBox()
		rfbox.set_border_width(5)
		okbutton=gtk.Button('ОК')
		cancelbutton=gtk.Button('Отмена')
		cancelbutton.connect('clicked',self.__on_click,'close')
		sendbutton=gtk.Button('PC -> Весы')
		sendbutton.connect('clicked',self.__on_click,'sendcale')
		recivebutton=gtk.Button('Весы -> РС')
		recivebutton.connect('clicked',self.__on_click,'resivescale')
		rfbox.add(okbutton)
		rfbox.add(cancelbutton)
		rfbox.add(sendbutton)
		rfbox.add(recivebutton)
		hbox.pack_start(rfbox,False,True,4)
		self.add(hbox)
		self.show_all()
		pass

class SetScrollString(gtk.Frame):
	'''
	   бегущая строка
	'''
	def __on_click(self,widget,data=None):
		if data=='resivescale':
			selscale=sysfrm.SelectScale()
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False	
			
			tigerlib.getScrollString_213()
			#self.semtry.set_text(text)			
		pass
		
	def __init__(self):
		gtk.Frame.__init__(self)
		self.set_label('Бегущая строка')
		hbox=gtk.HBox()
		lvb=gtk.VBox()
		lvb.pack_start(gtk.Label('Название магазина'),False,True)
		self.semtry=gtk.Entry(100)
		lvb.pack_start(self.semtry,False,True)
		hbox.pack_start(lvb,True,True,4)		
		
		vbox=gtk.VBox()
		sendbutton=gtk.Button('PC -> Весы')
		sendbutton.connect('clicked',self.__on_click,'sendscale')
		recivebutton=gtk.Button('Весы -> РС')
		recivebutton.connect('clicked',self.__on_click,'resivescale')
		vbox.pack_start(sendbutton,False,True,4)
		vbox.pack_start(recivebutton,False,True,4)
		hbox.pack_start(vbox,False,True,4)
		self.add(hbox)
		self.show_all()
		pass

class Colontitul(gtk.Frame):
	'''
	  Верхний и нижний колонтитулы
	'''
	def __on_click(self,widget,data=None):
		if data=='resivescale':
			selscale=sysfrm.SelectScale(1)
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False
			
			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						num,font_size,text=tigerlib.getHeaders_211(0)
						if num==0 :
							self.upedit.set_text(text)
							self.up_size.set_text(font_size)
						time.sleep(1)
						num,font_size,text=tigerlib.getHeaders_211(1)
						if num==1:
							self.dwnedit.set_text(text)
							self.dwn_size.set_text(font_size)
			pass
			
		if data=='sendscale':
			selscale=sysfrm.SelectScale()
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False

			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						tigerlib.setHeaders_211(0,self.up_size.get_text(),self.upedit.get_text())
						time.sleep(1)
						tigerlib.setHeaders_211(1,self.dwn_size.get_text(),self.dwnedit.get_text())
			pass
		pass
		
	def __init__(self):
		gtk.Frame.__init__(self)
		self.set_label('Верхний и нижние колонтитулы')
		hbox=gtk.HBox()
		lvb=gtk.VBox()
		self.upedit=gtk.Entry(140)
		self.dwnedit=gtk.Entry(140)
		lvb.pack_start(gtk.Label('Вехний колонтитул'),False,True,4)
		lvb.pack_start(self.upedit,False,True,4)
		hsize1=gtk.HBox(False)
		hsize1.pack_start(gtk.Label('Размер фонта (0-9, A-K)'),True,True,2)
		self.up_size=gtk.Entry(1)
		hsize1.pack_start(self.up_size,False,True,2)
		lvb.pack_start(hsize1,False,True,4)
		lvb.pack_start(gtk.Label('Нижний колонтитул'),False,True,4)
		lvb.pack_start(self.dwnedit,False,True,4)
		hsize1=gtk.HBox(False)
		hsize1.pack_start(gtk.Label('Размер фонта (0-9, A-K)'),True,True,2)
		self.dwn_size=gtk.Entry(1)
		hsize1.pack_start(self.dwn_size,False,True,2)
		lvb.pack_start(hsize1,False,True,4)		
		rvb=gtk.VBox()
		sendbutton=gtk.Button('PC -> Весы')
		sendbutton.connect('clicked',self.__on_click,'sendscale')
		recivebutton=gtk.Button('Весы -> РС')
		recivebutton.connect('clicked',self.__on_click,'resivescale')
		rvb.pack_start(sendbutton,False,True,4)
		rvb.pack_start(recivebutton,False,True,4)		
		hbox.pack_start(lvb,True,True,10)
		hbox.pack_start(rvb,False,True)
		
		self.add(hbox)
		self.show_all()
		
class SetShopName(gtk.Frame):
	'''
	   Название магазина
	'''
	def __on_click(self,widget,data=None):
		if data=='sendscale':
			selscale=sysfrm.SelectScale()
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False
			
			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						tigerlib.setOrganisation_212(self.semtry.get_text())
			pass
			
		if data=='resivescale':
			selscale=sysfrm.SelectScale(1)
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False			
			
			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						num,text=tigerlib.getOrganisation_212()
						self.semtry.set_text(text)
			pass
			
		pass
		
	def __init__(self):
		gtk.Frame.__init__(self)
		self.set_label('Название магазина')
		hbox=gtk.HBox()
		lvb=gtk.VBox()
		lvb.pack_start(gtk.Label('Название магазина'),False,True)
		self.semtry=gtk.Entry(70)
		lvb.pack_start(self.semtry,False,True)
		hbox.pack_start(lvb,True,True,4)
		vbox=gtk.VBox()
		sendbutton=gtk.Button('PC -> Весы')
		sendbutton.connect('clicked',self.__on_click,'sendscale')
		recivebutton=gtk.Button('Весы -> РС')
		recivebutton.connect('clicked',self.__on_click,'resivescale')
		vbox.pack_start(sendbutton,False,True,4)
		vbox.pack_start(recivebutton,False,True,4)
		hbox.pack_start(vbox,False,True,4)
		self.add(hbox)
		self.show_all()
		pass

class SetReclamText(gtk.Frame):
	'''
	   Рекламный текст
	'''
	
	def __clear_text(self):
		for i in xrange(1,2000):
			if glu.testKey('Rec Num '+str(i)):
				glu.delKey('Rec Num '+str(i))
				glu.delKey('Rec Text '+str(i))

		
	def __on_click(self,widget,data=None):
		if data=='new':
			if len(self.mes.get_text())!=0:
				glu.setKey('Rec Num '+self.num.get_text(),int(self.num.get_text()))
				glu.setKey('Rec Text '+self.num.get_text(),self.mes.get_text())
				self.__refresh()
				pass
			pass
		if data=='del':
			if len(self.num.get_text())!=0:
				glu.delKey('Rec Num '+self.num.get_text())
				glu.delKey('Rec Text '+self.num.get_text())
				self.num.set_text('')
				self.mes.set_text('')
				self.__refresh()
		if data=='resivescale':
			selscale=sysfrm.SelectScale()
			selscale.run()
			selscale.destroy()			
			
			self.__clear_text()
			for i in xrange(1,20): #2000
				try :
					num,txt=tigerlib.getMoreText_209(i)
					glu.setKey('Rec Num '+str(num),num)
					glu.setKey('Rec Text '+str(num),txt)
				except :
					print 'поймали'
					continue
				time.sleep(1)
			self.__refresh()
		if data=='sendcale':
			pass
		pass
		
	def __on_row_activated(self,widget,row,col):
		tree_model,tree_iter=widget.get_selection().get_selected()
		if tree_iter!=None:
			id=tree_model.get_value(tree_iter,0)
			self.num.set_text(glu.getKey('Rec Num '+str(id)))
			self.mes.set_text(glu.getKey('Rec Text '+str(id)))
			pass
		pass
	def __on_row_selected(self,widget):
		pass
		
	def __refresh(self):
		self.lst.clear()
		for i in xrange(1,2000):
			if glu.testKey('Rec Text '+str(i)):
				self.lst.append([int(glu.getKey('Rec Num '+str(i))),glu.getKey('Rec Text '+str(i))])
			pass
		pass
			
	def __set_tree(self):
		self.lst=gtk.ListStore(int,str)
		tree=gtk.TreeView(self.lst)
		tree.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
		tree.connect('cursor-changed',self.__on_row_selected)
		tree.connect('row-activated',self.__on_row_activated)
		renderText=gtk.CellRendererText()
		column=gtk.TreeViewColumn('#',renderText,text=0)
		tree.append_column(column)
		column=gtk.TreeViewColumn('Дополнительный текст',renderText,text=1)
		tree.append_column(column)		
		self.__refresh()
		return tree		
		
	def __dwn_lf_panel(self):
		dp=gtk.HBox()
		self.num=gtk.Entry(4)
		self.mes=gtk.Entry(200)
		dp.pack_start(self.num,False,False,4)
		dp.pack_start(self.mes,True,True,4)
		bt1=gtk.Button('Добавить')
		bt1.connect('clicked',self.__on_click,'new')
		bt2=gtk.Button('Удалить')
		bt2.connect('clicked',self.__on_click,'del')
		dp.pack_start(bt1,False,True,4)
		dp.pack_start(bt2,False,True,4)
		return dp		
	
	
		
	def __init__(self):
		gtk.Frame.__init__(self)
		self.set_label('Рекламный текст')
		hbox=gtk.HBox()
		lfbox=gtk.VBox()
		lfbox.pack_start(self.__set_tree(),True,True,4)
		lfbox.pack_start(self.__dwn_lf_panel(),False,True,4)
		hbox.pack_start(lfbox,True,True,4)
		rfbox=gtk.VButtonBox()
		rfbox.set_border_width(5)
		okbutton=gtk.Button('ОК')
		cancelbutton=gtk.Button('Отмена')
		cancelbutton.connect('clicked',self.__on_click,'close')
		sendbutton=gtk.Button('PC -> Весы')
		sendbutton.connect('clicked',self.__on_click,'sendcale')
		recivebutton=gtk.Button('Весы -> РС')
		recivebutton.connect('clicked',self.__on_click,'resivescale')
		rfbox.add(okbutton)
		rfbox.add(cancelbutton)
		rfbox.add(sendbutton)
		rfbox.add(recivebutton)
		hbox.pack_start(rfbox,False,True,4)
		self.add(hbox)
		self.show_all()
		pass
		
class SetDocText(gtk.Frame):
	''' дополнительные тексты (ингридиенты) '''
	
	def __clear_text(self):
		for i in xrange(1,2000):
			if glu.testKey('Dop Num '+str(i)):
				glu.delKey('Dop Num '+str(i))
				glu.delKey('Dop Text '+str(i))

		
	def __on_click(self,widget,data=None):
		if data=='new':
			if len(self.mes.get_text())!=0:
				glu.setKey('Dop Num '+self.num.get_text(),int(self.num.get_text()))
				glu.setKey('Dop Text '+self.num.get_text(),self.mes.get_text())
				self.__refresh()
				pass
			pass
		if data=='del':
			if len(self.num.get_text())!=0:
				glu.delKey('Dop Num '+self.num.get_text())
				glu.delKey('Dop Text '+self.num.get_text())
				self.num.set_text('')
				self.mes.set_text('')
				self.__refresh()
		if data=='resivescale':
			selscale=sysfrm.SelectScale(1,title='прием')
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False			
			
			self.__clear_text()
			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						tigerlib.opensocket()
						for i in xrange(1,2000): 
						  try :
						  		num,txt=tigerlib.getMoreText_209(i,tigerlib.MULTIOPERATION)
						  		glu.setKey('Dop Num '+str(num),num)
						  		glu.setKey('Dop Text '+str(num),txt)
						  except :
						  	print 'поймали'
						  	continue
						  	#time.sleep(1)
						tigerlib.closesocket()
			self.__refresh()
		if data=='sendcale':
			selscale=sysfrm.SelectScale(title='передача')
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False
			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						tigerlib.opensocket()
						for i in xrange(1,2000):
							if glu.testKey('Dop Text '+str(i)):
								tigerlib.setMoreText_209(int(glu.getKey('Dop Num '+str(i))),glu.getKey('Dop Text '+str(i)),tigerlib.MULTIOPERATION)
								#time.sleep(1)
							pass
						tigerlib.closesocket()			
			pass
		pass
		
	def __on_row_activated(self,widget,row,col):
		tree_model,tree_iter=widget.get_selection().get_selected()
		if tree_iter!=None:
			id=tree_model.get_value(tree_iter,0)
			self.num.set_text(glu.getKey('Dop Num '+str(id)))
			self.mes.set_text(glu.getKey('Dop Text '+str(id)))
			pass
		pass
	def __on_row_selected(self,widget):
		pass
		
	def __refresh(self):
		self.lst.clear()
		for i in xrange(1,2000):
			if glu.testKey('Dop Text '+str(i)):
				self.lst.append([int(glu.getKey('Dop Num '+str(i))),glu.getKey('Dop Text '+str(i))])
			pass
		pass
			
	def __set_tree(self):
		self.lst=gtk.ListStore(int,str)
		tree=gtk.TreeView(self.lst)
		tree.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
		tree.connect('cursor-changed',self.__on_row_selected)
		tree.connect('row-activated',self.__on_row_activated)
		renderText=gtk.CellRendererText()
		column=gtk.TreeViewColumn('#',renderText,text=0)
		tree.append_column(column)
		column=gtk.TreeViewColumn('Дополнительный текст',renderText,text=1)
		tree.append_column(column)		
		self.__refresh()
		sr=gtk.ScrolledWindow()
		sr.add(tree)
		sr.show_all()
		return sr	
		
	def __dwn_lf_panel(self):
		dp=gtk.HBox()
		self.num=gtk.Entry(4)
		self.mes=gtk.Entry(200)
		dp.pack_start(self.num,False,False,4)
		dp.pack_start(self.mes,True,True,4)
		bt1=gtk.Button('Добавить')
		bt1.connect('clicked',self.__on_click,'new')
		bt2=gtk.Button('Удалить')
		bt2.connect('clicked',self.__on_click,'del')
		dp.pack_start(bt1,False,True,4)
		dp.pack_start(bt2,False,True,4)
		return dp	
	
	def __init__(self):
		gtk.Frame.__init__(self)
		self.set_label('Дополнительные тексты (ингридиенты)')
		hbox=gtk.HBox()
		lfbox=gtk.VBox()
		lfbox.pack_start(self.__set_tree(),True,True,4)
		lfbox.pack_start(self.__dwn_lf_panel(),False,True,4)
		hbox.pack_start(lfbox,True,True,4)
		rfbox=gtk.VButtonBox()
		rfbox.set_border_width(5)
		okbutton=gtk.Button('ОК')
		okbutton.set_sensitive(False)
		cancelbutton=gtk.Button('Отмена')
		cancelbutton.set_sensitive(False)
		cancelbutton.connect('clicked',self.__on_click,'close')
		sendbutton=gtk.Button('PC -> Весы')
		sendbutton.connect('clicked',self.__on_click,'sendcale')
		recivebutton=gtk.Button('Весы -> РС')
		recivebutton.connect('clicked',self.__on_click,'resivescale')
		rfbox.add(okbutton)
		rfbox.add(cancelbutton)
		rfbox.add(sendbutton)
		rfbox.add(recivebutton)
		hbox.pack_start(rfbox,False,True,4)
		self.add(hbox)
		self.show_all()
		
class SetTare(gtk.Frame):
	'''
	   Тара 
	'''
	def __on_click(self,widgth,data=None):
		if data=='new':
			if len(self.mes.get_text())!=0:
				glu.setKey('Tare Num '+self.num.get_text(),int(self.num.get_text()))
				glu.setKey('Tare '+self.num.get_text(),self.mes.get_text())
				self.__refresh()
				pass			
			pass
			
		pass
	
	def __refresh(self):
		self.lst.clear()
		for i in xrange(1,16):
			if glu.testKey('Tare '+str(i)):
				self.lst.append([int(glu.getKey('Tare Num '+str(i))),glu.getKey('Tare '+str(i))])
			pass
		pass	
	
	def __set_tree(self):
		self.lst=gtk.ListStore(int,float)
		tree=gtk.TreeView(self.lst)
		tree.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
		#tree.connect('cursor-changed',self.__on_row_selected)
		#tree.connect('row-activated',self.__on_row_activated)
		renderText=gtk.CellRendererText()
		column=gtk.TreeViewColumn('#',renderText,text=0)
		tree.append_column(column)
		column=gtk.TreeViewColumn('Тара',renderText,text=1)
		tree.append_column(column)		
		self.__refresh()
		sr=gtk.ScrolledWindow()
		sr.add(tree)
		sr.show_all()
		return sr		
	
	def __dwn_lf_panel(self):
		dp=gtk.HBox()
		self.num=gtk.Entry(4)
		self.mes=gtk.Entry(200)
		dp.pack_start(self.num,False,False,4)
		dp.pack_start(self.mes,True,True,4)
		bt1=gtk.Button('Добавить')
		bt1.connect('clicked',self.__on_click,'new')
		bt2=gtk.Button('Удалить')
		bt2.connect('clicked',self.__on_click,'del')
		dp.pack_start(bt1,False,True,4)
		dp.pack_start(bt2,False,True,4)
		return dp	
	
	def __init__(self):
		gtk.Frame.__init__(self)
		self.set_label('Тара (таблица значений) ')		
		hbox=gtk.HBox()
		
		hbox=gtk.HBox()
		lfbox=gtk.VBox()
		lfbox.pack_start(self.__set_tree(),True,True,4)
		lfbox.pack_start(self.__dwn_lf_panel(),False,True,4)
		hbox.pack_start(lfbox,True,True,4)
		rfbox=gtk.VButtonBox()
		rfbox.set_border_width(5)
		okbutton=gtk.Button('ОК')
		okbutton.set_sensitive(False)
		cancelbutton=gtk.Button('Отмена')
		cancelbutton.set_sensitive(False)
		cancelbutton.connect('clicked',self.__on_click,'close')
		sendbutton=gtk.Button('PC -> Весы')
		sendbutton.connect('clicked',self.__on_click,'sendcale')
		recivebutton=gtk.Button('Весы -> РС')
		recivebutton.connect('clicked',self.__on_click,'resivescale')
		rfbox.add(okbutton)
		rfbox.add(cancelbutton)
		rfbox.add(sendbutton)
		rfbox.add(recivebutton)
		hbox.pack_start(rfbox,False,True,4)		
		
		self.add(hbox)
		self.show_all()
		pass
		
class SetPlu(gtk.Frame):
	'''
	  Cписок товаров
	'''
	def __on_click(self,widgeth,data=None):
		if data=='load':
			dialog=gtk.FileChooserDialog('Открыть',None,gtk.FILE_CHOOSER_ACTION_OPEN,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OK,gtk.RESPONSE_OK))
			dialog.set_default_response(gtk.RESPONSE_OK)
			filter=gtk.FileFilter()
			filter.set_name('Список товаров')
			filter.add_pattern('*.csv')
			dialog.add_filter(filter)
			response=dialog.run()
			if response==gtk.RESPONSE_OK:
				self.__load_csv(dialog.get_filename())
				pass
			dialog.destroy()
		if data=='save':
			dialog=gtk.FileChooserDialog('Сохранить',None,gtk.FILE_CHOOSER_ACTION_SAVE,(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OK,gtk.RESPONSE_OK))
			dialog.set_default_response(gtk.RESPONSE_OK)
			filter=gtk.FileFilter()
			filter.set_name('Список товаров')
			filter.add_pattern('*.csv')
			dialog.add_filter(filter)
			response=dialog.run()
			if response==gtk.RESPONSE_OK:
				self.__save_cvs(dialog.get_filename())
				pass
			dialog.destroy()			
		
		if data=='sendcale':
			selscale=sysfrm.SelectScale()
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False
			
			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						tigerlib.opensocket()
						for l in self.lst:
							#tigerlib.setPLU_207(plu,barcode,name_plu,price,tax,tarenum,fixscale=0,group=0,flg=0,timegod=499,timesale=499,misctext=0,modestr=1)
							tigerlib.setPLU_207(l[0],l[1],l[2],l[4],0,0,timesale=l[5],timegod=l[6],misctext=l[7],modesocket=tigerlib.MULTIOPERATION,modestr=glu.getKey('Number line '+str(ci+1)))
						tigerlib.closesocket()		
			pass
				
		if data=='resivescale':
			selscale=sysfrm.SelectScale(1)
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False
				
			self.lst.clear()
			glu.pludata=[]
			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						tigerlib.opensocket()
						for i in xrange (1,2000):
							rt=tigerlib.getPLU_207(i,tigerlib.MULTIOPERATION)
							self.lst.append([int(rt[0]),rt[1],rt[2],0,float(rt[3]),int(rt[4]),int(rt[5]),int(rt[10])])
							glu.pludata.append([int(rt[0]),rt[1],rt[2],0,float(rt[3]),int(rt[4]),int(rt[5]),int(rt[10])])
							#time.sleep(1)
							pass
						tigerlib.closesocket()							
			pass
			
		if data=='new':
			#plu=NewPlu()
			#plu.set_default_response(gtk.RESPONSE_OK)
			#response=plu.run()
			self.lst.append(None)
			pass
		if data=='del':
			
			pass
			
		
		pass
		
	def __on_row_selected(self,widget):
		tree_model,tree_iter=widget.get_selection().get_selected()
		if tree_iter!=None:
			self.sel_id=tree_model.get_value(tree_iter,0)
			pass		
		pass
		
	def __load_csv(self,filename=None):
		# загрузка списка карточек
		if (filename==None) :
			return
		self.lst.clear()
		f=open(filename,'r')
		try:
			csvread=csv.reader(f)
			for row in csvread:
				self.lst.append([int(row[0]),row[1],row[2],int(row[3]),float(row[4]),int(row[5]),int(row[6]),int(row[7])])
				glu.pludata.append([int(row[0]),row[1],row[2],int(row[3]),float(row[4]),int(row[5]),int(row[6]),int(row[7])])
				pass
		finally:
			f.close()
		
		# востанавлиеваем привязки кнопок
		
		#fname=filename+'_key'+'.key'
		fname=filename+'_key'
		if os.access(fname,os.F_OK):
			glu.keyplulink={}
			#f=open(filename,'r')
			#print glu.keyplulink
			#m=pickle.load(f)
			#f.close()
			f=open(fname,'r')
			csvread=csv.reader(f)
			for row in csvread:
				glu.keyplulink[row[0]]=[row[1],row[2]]
			f.close()
		return
		pass
	
	def __save_cvs(self,filename=None):
		if (filename==None):
			return
		if filename.count('.csv')==0:
			filename=filename+'.csv'
			
		f=open(filename,'w')
		try:
			csvwrite=csv.writer(f,quoting=csv.QUOTE_NONNUMERIC)
			for l in self.lst:
				csvwrite.writerow(l)
				pass
		finally:
			f.close()
		# сохраняем привязки кнопок 
		#TODO  переделать
		if len(glu.keyplulink)!=0:
		#	print len(glu.keyplulink)
			f=open(filename+'_key'+'.key','w')
			pick=pickle.Pickler(f)
			pick.dump(glu.keyplulink)
			f.close()
			pass
			f=open(filename+'_key','w')
			csvwrite=csv.writer(f,quoting=csv.QUOTE_NONNUMERIC)
			for l in glu.keyplulink:
				csvwrite.writerow([l,glu.keyplulink[l][0],glu.keyplulink[l][1]])
			f.close() 
			
		pass
	
	# def col0_edited_cb( self, cell, path, new_text, model ):
        """
        Called when a text cell is edited.  It puts the new text
        in the model so that it is displayed properly.
        """
    #    print "Change '%s' to '%s'" % (model[path][0], new_text)
    #    model[path][0] = new_text
    #    return
	
	def __edit_col(self,cell,path,new_text,model,col=0):
		if type(model[path][col])==int:
			model[path][col]=int(new_text)
		elif type(model[path][col])==float :
			model[path][col]=float(new_text)
		else :
			model[path][col]=new_text
		return
			
	def __set_grid(self):
		# plu,barcode,name,группа,цена,срок реализации(дни),доп текст (ингридиетн)
		self.lst=gtk.ListStore(int,str,str,int,float,int,int,int)
		self.grid=gtk.TreeView(self.lst)
		self.grid.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
		self.grid.connect('cursor-changed',self.__on_row_selected)
		#treesel=self.grid.get_selection().set_mode(gtk.SELECTION_BROWSE)
		#self.grid=treesel.get_treeview()
		renderText=gtk.CellRendererText()
		renderText.set_property( 'editable', True )
		renderText.connect('edited',self.__edit_col,self.lst,0)
		cell=gtk.TreeViewColumn('PLU',renderText,text=0)
		cell.set_sort_column_id(0)  # включаем сортировку для колонке
		self.grid.append_column(cell)
		
		renderText=gtk.CellRendererText()
		renderText.set_property( 'editable', True )
		renderText.connect('edited',self.__edit_col,self.lst,1)
		
		cell=gtk.TreeViewColumn('Штрихкод',renderText,text=1)
		self.grid.append_column(cell)
		
		renderText=gtk.CellRendererText()
		renderText.set_property( 'editable', True )
		renderText.connect('edited',self.__edit_col,self.lst,2)
		
		cell=gtk.TreeViewColumn('Наименование',renderText,text=2)
		self.grid.append_column(cell)
		
		renderText=gtk.CellRendererText()
		renderText.set_property( 'editable', True )
		renderText.connect('edited',self.__edit_col,self.lst,3)
		
		cell=gtk.TreeViewColumn('Группа',renderText,text=3)
		self.grid.append_column(cell)
		
		renderText=gtk.CellRendererText()
		renderText.set_property( 'editable', True )
		renderText.connect('edited',self.__edit_col,self.lst,4)
		
		cell=gtk.TreeViewColumn('Цена',renderText,text=4)
		self.grid.append_column(cell)
		
		renderText=gtk.CellRendererText()
		renderText.set_property( 'editable', True )
		cell=gtk.TreeViewColumn('Срок реализации',renderText,text=5)
		renderText.connect('edited',self.__edit_col,self.lst,5)
		self.grid.append_column(cell)
		
		renderText=gtk.CellRendererText()
		renderText.set_property( 'editable', True )		
		cell=gtk.TreeViewColumn('Срок годности',renderText,text=6)
		renderText.connect('edited',self.__edit_col,self.lst,6)
		self.grid.append_column(cell)
		
		renderText=gtk.CellRendererText()
		renderText.set_property( 'editable', True )		
		cell=gtk.TreeViewColumn('Доп. текст',renderText,text=7)
		renderText.connect('edited',self.__edit_col,self.lst,7)
		self.grid.append_column(cell)		
						
		sr=gtk.ScrolledWindow()
		sr.add(self.grid)
		sr.show_all()
		return sr
		
	def __set_key_panel(self):
		btp=gtk.HButtonBox()
		btp.set_layout(gtk.BUTTONBOX_SPREAD)
		button=gtk.Button('Добавить')
		button.connect('clicked',self.__on_click,'new')
		btp.add(button)
		button=gtk.Button('Удалить')
		button.connect('clicked',self.__on_click,'del')
		btp.add(button)
		button=gtk.Button('Загрузить')
		button.connect('clicked',self.__on_click,'load')		
		btp.add(button)
		button=gtk.Button('Сохранить')
		button.connect('clicked',self.__on_click,'save')
		btp.add(button)
		button=gtk.Button('Весы -> PC')
		button.connect('clicked',self.__on_click,'resivescale')
		btp.add(button)
		button=gtk.Button('РС -> Весы')
		button.connect('clicked',self.__on_click,'sendcale')		
		btp.add(button)
		return btp
		
	def __init__(self):
		gtk.Frame.__init__(self)
		self.set_label('Карточки')
		vbox=gtk.VBox()
		vbox.pack_start(self.__set_grid(),True,True,4)
		vbox.pack_start(self.__set_key_panel(),False,True,4)
		self.add(vbox)
		if len(glu.pludata)!=0:
			for l in glu.pludata:
				self.lst.append([l[0],l[1],l[2],l[3],l[4],l[5],l[6],l[7]])
		self.show_all()
		pass

class SetPerson(gtk.Frame):
	'''
	   Продавцы
	'''
	def __clear_text(self):
		for i in xrange(1,99):
			if glu.testKey('Pers Num '+str(i)):
				glu.delKey('Pers Num '+str(i))
				glu.delKey('Pers Text '+str(i))
				
	def __on_click(self,widget,data=None):
		if data=='resivescale':
			selscale=sysfrm.SelectScale(1)
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False	
			
			self.__clear_text()
			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						tigerlib.opensocket()
						for i in xrange(1,99):
							try :
								num,txt=tigerlib.getSellers_204(i,modesocket=tigerlib.MULTIOPERATION)
								glu.setKey('Pers Num '+str(num),num)
								glu.setKey('Pers Text '+str(num),txt)
							except Exception,ecx :
								print 'поймали ',ecx
								continue
							#time.sleep(1)
						tigerlib.closesocket()
			self.__refresh()
			
		if data=='sendcale':
			selscale=sysfrm.SelectScale()
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False	
			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						tigerlib.opensocket()
						for i in xrange(1,99):
							if glu.testKey('Pers Text '+str(i)):
								tigerlib.setSellers_204(int(glu.getKey('Pers Num '+str(i))),glu.getKey('Pers Text '+str(i)),modesocket=tigerlib.MULTIOPERATION)
								#time.sleep(1)
						tigerlib.closesocket()			
			
		if data=='new'	:
			if len(self.num.get_text())!=0:
				ic=len(self.lst)
				ic +=1
				glu.setKey('Pers Num '+str(ic),self.num.get_text())
				glu.setKey('Pers Text '+str(ic),self.mes.get_text())
				self.__refresh()
		if data=='del':
			if len(self.num.get_text())!=0:
				glu.delKey('Pers Num '+self.num.get_text())
				glu.delKey('Pers Text '+self.num.get_text())
				self.num.set_text('')
				self.mes.set_text('')
				self.__refresh()			
			pass

     
	def __on_row_activated(self,widget,row,col):
		tree_model,tree_iter=widget.get_selection().get_selected()
		if tree_iter!=None:
			id=tree_model.get_value(tree_iter,0)
			self.num.set_text(glu.getKey('Pers Num '+str(id)))
			self.mes.set_text(glu.getKey('Pers Text '+str(id)))
			pass
		pass
	def __on_row_selected(self,widget):
		pass
		
	def __refresh(self):
	#	print self.lst
	#	print glu.prop
		self.lst.clear()
		for i in xrange(1,99):
			if glu.testKey('Pers Text '+str(i)):
				self.lst.append([int(glu.getKey('Pers Num '+str(i))),glu.getKey('Pers Text '+str(i))])
			pass
		pass
			
	def __set_tree(self):
		self.lst=gtk.ListStore(int,str)
		tree=gtk.TreeView(self.lst)
		tree.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
		tree.connect('cursor-changed',self.__on_row_selected)
		tree.connect('row-activated',self.__on_row_activated)
		renderText=gtk.CellRendererText()
		column=gtk.TreeViewColumn('#',renderText,text=0)
		tree.append_column(column)
		column=gtk.TreeViewColumn('Продавцы ',renderText,text=1)
		tree.append_column(column)		
		self.__refresh()
		sr=gtk.ScrolledWindow()
		sr.add(tree)
		sr.show_all()
		return sr	
		
	def __dwn_lf_panel(self):
		dp=gtk.HBox()
		self.num=gtk.Entry(4)
		self.mes=gtk.Entry(200)
		dp.pack_start(self.num,False,False,4)
		dp.pack_start(self.mes,True,True,4)
		bt1=gtk.Button('Добавить')
		bt1.connect('clicked',self.__on_click,'new')
		bt2=gtk.Button('Удалить')
		bt2.connect('clicked',self.__on_click,'del')
		dp.pack_start(bt1,False,True,4)
		dp.pack_start(bt2,False,True,4)
		return dp	
	
	def __init__(self):
		gtk.Frame.__init__(self)
		self.set_label('Продавцы')
		hbox=gtk.HBox()
		lfbox=gtk.VBox()
		lfbox.pack_start(self.__set_tree(),True,True,4)
		lfbox.pack_start(self.__dwn_lf_panel(),False,True,4)
		hbox.pack_start(lfbox,True,True,4)
		rfbox=gtk.VButtonBox()
		rfbox.set_border_width(5)
		okbutton=gtk.Button('ОК')
		okbutton.set_sensitive(False)
		cancelbutton=gtk.Button('Отмена')
		cancelbutton.set_sensitive(False)
		cancelbutton.connect('clicked',self.__on_click,'close')
		sendbutton=gtk.Button('PC -> Весы')
		sendbutton.connect('clicked',self.__on_click,'sendcale')
		recivebutton=gtk.Button('Весы -> РС')
		recivebutton.connect('clicked',self.__on_click,'resivescale')
		rfbox.add(okbutton)
		rfbox.add(cancelbutton)
		rfbox.add(sendbutton)
		rfbox.add(recivebutton)
		hbox.pack_start(rfbox,False,True,4)		
		
		self.add(hbox)
		self.show_all()
		pass

class SetGroup(gtk.Frame):
	''' группы товаров '''
	
	def __clear_text(self):
		for i in xrange(1,20):
			if glu.testKey('Group Num '+str(i)):
				glu.delKey('Group Num '+str(i))
				glu.delKey('Group Text '+str(i))
				
	def __on_click(self,widget,data=None):
		if data=='new':
			if len(self.num.get_text())!=0:
				ic=len(self.lst)
				ic +=1
				if ic>20:
					return False
				glu.setKey('Group Num '+str(ic),self.num.get_text())
				glu.setKey('Group Text '+str(ic),self.mes.get_text())
				self.__refresh()			
			pass
		if data=='del':
			pass
		if data=='sendcale':
			selscale=sysfrm.SelectScale()
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False
			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						tigerlib.opensocket()
						for i in xrange(1,20):
							if glu.testKey('Group Text '+str(i)):
								tigerlib.setCommodityGroups_210(int(glu.getKey('Group Num '+str(i))),glu.getKey('Group Text '+str(i)),int(glu.getKey('Group Num '+str(i))),modesocket=tigerlib.MULTIOPERATION)
								#time.sleep(1)
						tigerlib.closesocket()
			pass
		if data=='resivescale':
			selscale=sysfrm.SelectScale(1)
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False	
			
			self.__clear_text()
			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						tigerlib.opensocket()
						for i in xrange(1,20):
							try :
								num,txt,root_group=tigerlib.getCommodityGroups_210(i,tigerlib.MULTIOPERATION)
								glu.setKey('Group Num '+str(i),num)
								glu.setKey('Group Text '+str(i),txt)
							except Exception,ecx :
								print 'поймали ',ecx
								continue
								#time.sleep(1)
						tigerlib.closesocket()
			self.__refresh()			
			pass
		pass
	
	def __on_row_activated(self,widget,row,col):
		tree_model,tree_iter=widget.get_selection().get_selected()
		if tree_iter!=None:
			id=tree_model.get_value(tree_iter,0)
			self.num.set_text(glu.getKey('Group Num '+str(id)))
			self.mes.set_text(glu.getKey('Group Text '+str(id)))
			pass
		pass
	def __on_row_selected(self,widget):
		pass	
		
	def __refresh(self):
	#	print self.lst
	#	print glu.prop
		self.lst.clear()
		for i in xrange(1,20):
			if glu.testKey('Group Text '+str(i)):
				self.lst.append([int(glu.getKey('Group Num '+str(i))),glu.getKey('Group Text '+str(i))])
			pass
		pass
	def __set_tree(self):
		self.lst=gtk.ListStore(int,str)
		tree=gtk.TreeView(self.lst)
		tree.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
		tree.connect('cursor-changed',self.__on_row_selected)
		tree.connect('row-activated',self.__on_row_activated)
		renderText=gtk.CellRendererText()
		column=gtk.TreeViewColumn('#',renderText,text=0)
		tree.append_column(column)
		column=gtk.TreeViewColumn('Наименование группы',renderText,text=1)
		tree.append_column(column)
		self.__refresh()
		sr=gtk.ScrolledWindow()
		sr.add(tree)
		sr.show_all()
		return sr
		
	def __dwn_lf_panel(self):
		dp=gtk.HBox()
		self.num=gtk.Entry(4)
		self.mes=gtk.Entry(20)
		dp.pack_start(self.num,False,False,4)
		dp.pack_start(self.mes,True,True,4)
		bt1=gtk.Button('Добавить')
		bt1.connect('clicked',self.__on_click,'new')
		bt2=gtk.Button('Удалить')
		bt2.connect('clicked',self.__on_click,'del')
		dp.pack_start(bt1,False,True,4)
		dp.pack_start(bt2,False,True,4)
		return dp		
	
	def __init__(self):
		gtk.Frame.__init__(self)
		self.set_label('Группы товаров')
		hbox=gtk.HBox()
		lfbox=gtk.VBox()
		lfbox.pack_start(self.__set_tree(),True,True,4)
		lfbox.pack_start(self.__dwn_lf_panel(),False,True,4)
		hbox.pack_start(lfbox,True,True,4)
		
		rfbox=gtk.VButtonBox()
		rfbox.set_border_width(5)
		okbutton=gtk.Button('ОК')
		okbutton.set_sensitive(False)
		cancelbutton=gtk.Button('Отмена')
		cancelbutton.set_sensitive(False)
		cancelbutton.connect('clicked',self.__on_click,'close')
		sendbutton=gtk.Button('PC -> Весы')
		sendbutton.connect('clicked',self.__on_click,'sendcale')
		recivebutton=gtk.Button('Весы -> РС')
		recivebutton.connect('clicked',self.__on_click,'resivescale')
		rfbox.add(okbutton)
		rfbox.add(cancelbutton)
		rfbox.add(sendbutton)
		rfbox.add(recivebutton)
		hbox.pack_start(rfbox,False,True,4)			
		
		self.add(hbox)
		self.show_all()
		
class SetConfScale(gtk.Frame):
	''' конфигурация обслуживания '''
	
	rt=[]
	
	def __on_click(self,widget,data=None):
		if data=='resivescale':
			selscale=sysfrm.SelectScale(1)
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False
				
			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						tigerlib.opensocket()
						self.rt=tigerlib.getConfigWrk_202(modesocket=tigerlib.MULTIOPERATION)
						tigerlib.closesocket()
			pass
			self.__set_view_param()
		pass
	
	def __set_view_param(self):
	#	print self.rt
		if self.rt[6][11]==0:
			self.rb1.set_active(True)
		else :
			self.rb2.set_active(True)

		self.scrollstr.set_active(self.rt[5][15]==1)	
		self.ean.set_active(self.rt[5][0]==1)
		self.eantalon.set_active(self.rt[5][1]==1)
		self.sumscale.set_active(self.rt[5][2]==1)
		self.talon.set_active(self.rt[5][4]==1)
		self.upscroll.set_active(self.rt[5][5]==1)
		self.dwnscroll.set_active(self.rt[5][6]==1)
		self.no_shr_key.set_active(self.rt[6][4]==0)
		self.combo.set_active(self.rt[2])
		pass
		
	def __re(self):
		vbox=gtk.VBox()
		frm=gtk.Frame('Режим при включении питания')
		vb=gtk.VBox()
		self.rb1=gtk.RadioButton(None,'Обслуживание')
		self.rb2=gtk.RadioButton(self.rb1,'Предупаковка')
		vb.pack_start(self.rb1,False,True)
		vb.pack_start(self.rb2,False,True)
		frm.add(vb)
		vbox.pack_start(frm,False,True)
		vbox.pack_start(gtk.Label('Печать на носителе'),False,True,5)
		#self.combo=gtk.Combo()
		#self.combo.set_popdown_strings(['Чек','Этикетка','Этикетка + итог.','Чек на этикетке'])
		
		lst=gtk.ListStore(str)
		lst.append(['Чек'])
		lst.append(['Этикетка'])
		lst.append(['Этикетка + итог.'])
		lst.append(['Чек на этикетке'])
		cell = gtk.CellRendererText()
		self.combo=gtk.ComboBox(lst)
		self.combo.pack_start(cell,True)
		self.combo.add_attribute(cell, 'text', 0)
		
		vbox.pack_start(self.combo,False,True)
		self.scrollstr=gtk.CheckButton('Бегущая строка')
		vbox.pack_start(self.scrollstr,False,True,10)
		frm1=gtk.Frame('Ввод цены')
		vb=gtk.VBox()
		self.no_shr_key=gtk.RadioButton(None,'Не использовать #')
		vb.pack_start(self.no_shr_key,False,True)
		nsk=gtk.RadioButton(self.no_shr_key,'Использовать #')
		vb.pack_start(nsk,False,True)
		frm1.add(vb)
		vbox.pack_start(frm1,False,True,5)
		return vbox
	
	def __re_set(self):
		frm=gtk.Frame('Опции')
		vb=gtk.VBox()
		cb=gtk.CheckButton('Номер PLU')
		vb.pack_start(cb,False,True)
		self.ean=gtk.CheckButton('Штрих-код')
		vb.pack_start(self.ean,False,True)
		self.eantalon=gtk.CheckButton('Штрих-код на талоне')
		vb.pack_start(self.eantalon,False,True)
		self.sumscale=gtk.CheckButton('Суммарный вес')
		vb.pack_start(self.sumscale,False,True)
		cb=gtk.CheckButton('Этикетка #')
		vb.pack_start(cb,False,True)
		self.upscroll=gtk.CheckButton('Верхний текст')
		vb.pack_start(self.upscroll,False,True)		
		self.dwnscroll=gtk.CheckButton('Нижний текст')
		vb.pack_start(self.dwnscroll,False,True)										
		cb=gtk.CheckButton('Вес тары')
		vb.pack_start(cb,False,True)
		self.talon=gtk.CheckButton('Талон')
		vb.pack_start(self.talon,False,True)				
		frm.add(vb)
		return frm
		
	def _down_button(self):
		hb=gtk.HBox()
		hb.set_border_width(4)
		bt1=gtk.Button('Весы -> PC')
		bt1.connect('clicked',self.__on_click,'resivescale')
		bt2=gtk.Button('РС -> Весы')
		bt2.connect('clicked',self.__on_click,'sendcale')
		hb.pack_start(bt1,False,True,4)
		hb.pack_start(bt2,False,True,4)
		return hb
				
	def __init__(self):
		gtk.Frame.__init__(self)
		vbox=gtk.VBox()
		hbox=gtk.HBox()
		
		hbox.pack_start(self.__re(),False,True)
		hbox.pack_start(self.__re_set(),True,True)
		vbox.pack_start(hbox,True,True)
		vbox.pack_start(self._down_button(),False,True)
		self.add(vbox)
		self.show_all()
