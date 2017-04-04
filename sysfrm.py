#-*- coding: utf-8 -*-
import gtk,gobject
import glu

class SelectScale(gtk.Dialog):
	def __on_close(self,widget):
		self.ok_flg=False
		self.response(gtk.RESPONSE_CLOSE)
	
	def __on_click(self,widget,data=None):
		if data=='run':
			self.ok_flg=True
			self.response(gtk.RESPONSE_CLOSE)
			pass
			
		if data=='sellall':
			for i in xrange(0,len(self.lst)):
				glu.setKey('Exchange scale '+str(self.lst[i][0]),True)
			self.__refresh()
		if data=='delsall':
			for i in xrange(0,len(self.lst)):
				glu.setKey('Exchange scale '+str(self.lst[i][0]),False)				
			self.__refresh()
			
	def __test_one_rec(self,id):
		''' возвращает True если уже есть активный елемент'''
		for i in xrange(glu.getKey('Count Scale')):
			if glu.testKey('Exchange scale '+str(i+1)):
				if glu.getKey('Exchange scale '+str(i+1)) and (id!=(i+1)):
					return True
		return False
		
	def __on_row_activated(self,widget,row,col):
		tree_model,tree_iter=widget.get_selection().get_selected()
		if tree_iter!=None:
			id=tree_model.get_value(tree_iter,0)

			if self.select_multi_mode==1:
				if self.__test_one_rec(id) :
					return False
			if glu.testKey('Exchange scale '+str(id)):
				flg=not glu.getKey('Exchange scale '+str(id))
				glu.setKey('Exchange scale '+str(id),flg)
			else :
				glu.setKey('Exchange scale '+str(id),True)
			self.__refresh()
		#print row,id,col
		pass
		
	def __set_model(self):
		self.__set_default_select()
		self.lst=gtk.ListStore(int,str,str,gobject.TYPE_BOOLEAN)
		self.__refresh()
		return self.lst
		
	def __refresh(self):
		self.lst.clear()
		#print glu.prop
		for i in xrange(glu.getKey('Count Scale')):
			if glu.getKey('Scale use '+str(i+1)) :
				flg=True
				if glu.testKey('Exchange scale '+str(i+1)):
					flg=glu.getKey('Exchange scale '+str(i+1))
				print type(flg)
				self.lst.append([int(glu.getKey('Num '+str(i+1))),glu.getKey('Name Scale '+str(i+1)),glu.getKey('IP '+str(i+1)),flg])
	
	
	def __set_sel_box(self):
		hbox=gtk.HBox(False)
		sb=gtk.ScrolledWindow()
		grid=gtk.TreeView(self.__set_model())
		grid.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
		grid.connect('row-activated',self.__on_row_activated)
		
		renderText=gtk.CellRendererText()
		column=gtk.TreeViewColumn('#',renderText,text=0)
		grid.append_column(column)
		column=gtk.TreeViewColumn('Наименование',renderText,text=1)
		column.set_resizable(True)
		grid.append_column(column)
		column=gtk.TreeViewColumn('IP',renderText,text=2)
		grid.append_column(column)
		cellBoll=gtk.CellRendererToggle()
		#renderText=gtk.CellRendererText()
		cellBoll.set_property('activatable', True)
		#column=gtk.TreeViewColumn('Исп.',renderText,text=3,editable=2)
		column=gtk.TreeViewColumn('Исп.',cellBoll,active=3)

		grid.append_column(column)
		
		sb.add(grid)
		sb.show_all()
		hbox.pack_start(sb,True,True,4)
		vbutton=gtk.VButtonBox()
		runbutton=gtk.Button('Передача')
		runbutton.connect('clicked',self.__on_click,'run')
		selall=gtk.Button('Выбрать все')
		selall.connect('clicked',self.__on_click,'sellall')
		if self.select_multi_mode==1:
			selall.set_sensitive(False)
		deselectall=gtk.Button('Сбросить все')
		deselectall.connect('clicked',self.__on_click,'delsall')
		if self.select_multi_mode==1:
			deselectall.set_sensitive(False)
		vbutton.add(runbutton)
		vbutton.add(selall)
		vbutton.add(deselectall)
		hbox.pack_start(vbutton,False,True,4)
		return hbox
			
	def __set_default_select(self):
		for i in xrange(glu.getKey('Count Scale')):
			if glu.getKey('Scale use '+str(i+1)) :
				if glu.testKey('Exchange scale '+str(i+1))!=True:
					glu.setKey('Exchange scale '+str(i+1),False)

	def __init__(self,select_multi_mode=0,title=None):
		super(SelectScale,self).__init__()
		self.select_multi_mode=select_multi_mode
		if title!=None:
			self.set_title('Выбор весов для операции :'+title)
		else :
			self.set_title('Выбор весов для операции')
		self.set_default_size(600,300)
		self.vbox.pack_start(self.__set_sel_box(),True,True);
		closeBt=gtk.Button('Закрыть')
		closeBt.connect('clicked',self.__on_close)
		self.action_area.pack_end(closeBt,False,True,4)
		self.set_modal(True)
		self.show_all()
		pass

class ViewWorking():
	
	def __init__(self):
		pass
