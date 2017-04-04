#-*- coding:utf-8 -*-
import gtk
import glu
import sysfrm
import tigerlib
import re


class MyButton(gtk.DrawingArea):
	#  рамка фон 
	color_normal=['#2244a5','#597ada']
	color_enter=['#2244a5','#7e9aec']
	color_press=['#2244a5','#7e9aec']
	color_shema=color_normal
	text=''
	def __init__(self,text=None):
		gtk.DrawingArea.__init__(self)
		self.set_size_request(64,32)
		if text is not None:
			self.text=text
		self.pangolayout=self.create_pango_layout("")
		self.add_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.POINTER_MOTION_MASK |gtk.gdk.SCROLL_MASK | gtk.gdk.ENTER_NOTIFY_MASK | gtk.gdk.LEAVE_NOTIFY_MASK | gtk.gdk.KEY_PRESS_MASK)
		self.connect('expose_event',self.expose)
		self.connect('realize',self.realize)
		self.connect('enter-notify-event',self.enter_notify)
		self.connect('leave-notify-event',self.leave_notify)
		self.show_all()		
		pass
		
			
	def realize(self,area):
		self.gc=self.window.new_gc()
		self.colormap=self.window.get_colormap()	
		self.gc.line_width=2
		self.gc.set_foreground(self.colormap.alloc_color('#2244a5',True,True))	
		return True

	def expose(self,widget,event):
		x,y,width,height=self.get_allocation()
		#print width,height
		#print self.color_shema
		self.gc.set_foreground(self.colormap.alloc_color(self.color_shema[1],True,True))	
		self.window.draw_rectangle(self.gc,True,1,1,width-1,height-1)
		self.gc.set_foreground(self.colormap.alloc_color(self.color_shema[0],True,True))
		self.window.draw_rectangle(self.gc,False,1,1,width-2,height-2)
		if len(self.text)!=0:
			self.pangolayout.set_text(self.text)
			#print self.pangolayout.get_font_description()
			self.window.draw_layout(self.gc, width/2, height/4, self.pangolayout)
		return True
	def enter_notify(self,widget,event):
		self.color_shema=self.color_enter
		self.redraw()
		pass
		
	def leave_notify(self,widget,event):
		self.color_shema=self.color_normal
		self.redraw()
		pass
		
	def redraw(self,area=None):
		expose_event = gtk.gdk.Event(gtk.gdk.EXPOSE)
		expose_event.window=self.window
		if area is not None:
			expose_event.area=area
		else:
			rect=self.get_allocation()
			expose_event.area=gtk.gdk.Rectangle(0,0,rect.width,rect.height)
		self.send_expose(expose_event)		
		pass
				
	def setText(self,text):
		self.text=text
		#self.redraw()
		pass
	def getText(self):
		return self.text
		
class SelectPlu(gtk.Dialog):
	'''
	  Выбирает plu из загруженного списка для связывания с кнопкой
	'''
	def __on_close(self,widget):
		self.flg=False
		self.response(gtk.RESPONSE_CLOSE)
		
	def __on_click(self,widget,data=None):
		if self.sel_id!=-1:
			self.flg=True
		else :
			self.flg=False
		self.response(gtk.RESPONSE_CLOSE)	
	
	def __on_row_selected(self,widget):
		tree_model,tree_iter=widget.get_selection().get_selected()
		if tree_iter!=None:
			self.sel_id=tree_model.get_value(tree_iter,0)
			self.sel_name=tree_model.get_value(tree_iter,1)
			print self.sel_id,self.sel_name
			pass		
		pass			
		
	def __init__(self):
		super(SelectPlu,self).__init__()
		self.set_title('Выбор товара')
		self.set_default_size(480,200)
		self.set_size_request(480,200)
		#TODO поставить центрирование 
		sw=gtk.ScrolledWindow()
		self.lst=gtk.ListStore(int,str)
		for l in glu.pludata:
			self.lst.append([l[0],l[2]])
			pass
		self.sel_id=-1	
		self.grid=gtk.TreeView(self.lst)
		self.grid.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
		self.grid.connect('cursor-changed',self.__on_row_selected)
		renderText=gtk.CellRendererText()
		cell=gtk.TreeViewColumn('PLU',renderText,text=0)
		cell.set_sort_column_id(0)  # включаем сортировку для колонке
		self.grid.append_column(cell)
		renderText=gtk.CellRendererText()
		cell=gtk.TreeViewColumn('Наименование',renderText,text=1)
		self.grid.append_column(cell)
				
		sw.add(self.grid)
		self.vbox.pack_start(sw,True,True)
		run_bt=gtk.Button('Принять')
		run_bt.connect('clicked',self.__on_click)
		close_bt=gtk.Button('Закрыть')
		close_bt.connect('clicked',self.__on_close)
		self.action_area.pack_start(run_bt,False,True,4)
		self.action_area.pack_end(close_bt,False,True,4)
		self.show_all()

class setLinkKeyPlu(gtk.Dialog):
	'''
	   связь кнопки на весах и plu
	'''

			
	def __on_close(self,widget):
		self.flg=False
		self.response(gtk.RESPONSE_CLOSE)
		
	def __on_click(self,widget,data=None):
		if data=='select':
			sp=SelectPlu()
			sp.run()
			if sp.flg:
				self.card_name.set_text(sp.sel_name)
				self.sel_id=sp.sel_id
				pass
			sp.destroy()
		if data=='run':
			glu.keyplulink[self.sel_key_name]=[self.sel_id,self.card_name.get_text()]
			#print glu.keyplulink
			self.flg=True
			self.response(gtk.RESPONSE_CLOSE)
			pass
		pass
		
	
	def __init__(self):
		super(setLinkKeyPlu,self).__init__()
		self.set_title('Связывание программируемой кнопки')
		self.set_default_size(400,100)
		lb=gtk.Label('Выбраный товар :')
		self.vbox.pack_start(lb,False,True,2)
		hbox=gtk.HBox()
		self.card_name=gtk.Entry(80)
		bt=gtk.Button('...')
		bt.connect('clicked',self.__on_click,'select')
		hbox.pack_start(self.card_name,True,True)
		hbox.pack_start(bt,False,True,4)
		self.vbox.pack_start(hbox,False,True)
		run_bt=gtk.Button('Принять')
		run_bt.connect('clicked',self.__on_click,'run')
		self.action_area.pack_end(run_bt,False,True,4)
		close_bt=gtk.Button('Закрыть')
		close_bt.connect('clicked',self.__on_close)
		self.action_area.pack_end(close_bt,False,True,4)
		self.set_modal(True)
		self.show_all()
		pass
		

class SetKeyInPlu(gtk.Frame):
	# раскладка по умолчанию 100 клавишьная панель 10x10
	__row=10
	__column=10
	__mode_key=100
	
	def __init__(self):
		gtk.Frame.__init__(self)
		self.set_label('Редактор привязок кнопок к PLU')
		vbox=gtk.VBox()
		self.tb=gtk.Table(self.__row,self.__column)
		#mb=MyButton()
		#self.add(mb)
		top,left=0,0
		bottom,rigth=1,1
		itxt=1
		for j in xrange(self.__row):
			for i in xrange(self.__column):
				mb=MyButton(str(i))
				mb.connect('button-release-event',self.__on_click,'mb'+str(itxt))
				self.tb.attach(mb,left,rigth,top,bottom,xpadding=2,ypadding=2)
				if len(glu.keyplulink)!=0 and glu.keyplulink.has_key('mb'+str(itxt)) :
					mb.setText(str(itxt)+'/'+str(glu.keyplulink['mb'+str(itxt)][0]))
					mb.set_tooltip_text(glu.keyplulink['mb'+str(itxt)][1])
				else :
					mb.setText(str(itxt))
				left +=1
				rigth +=1				
				itxt +=1
			left=0
			rigth=1
			top +=1
			bottom +=1	
		vbox.add(self.tb)
		vbox.pack_start(self.__set_key_panel(),False,True,4)	
		self.add(vbox)	
		self.show_all()
		
	def __on_click_2(self,widget,data=None):
		#print widget,data
		#print glu.pludata
		if data=='resivescale':
			'''
			  данные из весов
			'''
			selscale=sysfrm.SelectScale(1)
			selscale.run()
			if selscale.ok_flg :
				selscale.destroy()
			else :
				selscale.destroy()
				return False
			glu.keyplulink.clear()
			for ci in xrange(glu.getKey('Count Scale')):
				if glu.testKey('Exchange scale '+str(ci+1)):
					if glu.getKey('Exchange scale '+str(ci+1)):
						tigerlib.address=glu.getKey('IP '+str(ci+1))
						tigerlib.opensocket()
						for i in xrange (1,100):
							rt=tigerlib.getFixKey_216(i,tigerlib.MULTIOPERATION)
							x=next((x for x in glu.pludata if x[0]==rt[2]),None)
							if x!=None:
								glu.keyplulink['mb'+str(rt[0])]=[str(rt[2]),x[2].encode('utf-8').rstrip('\x00')]
						tigerlib.closesocket()	
				pass
		if data=='sendcale':
			'''
			  данные в весы
			'''
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
						for l in glu.keyplulink:
							
							tigerlib.setFixKey_216(int(re.sub("[^0-9]","",l)),0,int(glu.keyplulink[l][0]),tigerlib.MULTIOPERATION)
							pass
						pass
						tigerlib.closesocket()		
						
			pass		
				
		pass
		
	def __set_key_panel(self):
		btp=gtk.HButtonBox()
		btp.set_layout(gtk.BUTTONBOX_SPREAD)
		button=gtk.Button('Весы -> PC')
		button.connect('clicked',self.__on_click_2,'resivescale')
		btp.add(button)
		button=gtk.Button('РС -> Весы')
		button.connect('clicked',self.__on_click_2,'sendcale')		
		btp.add(button)
		return btp
				
	def __on_click(self,widget,event,data=None):
		if event.button==1:
			slkp=setLinkKeyPlu()
			slkp.sel_key_name=data
			slkp.run()
			if slkp.flg:
				widget.setText(widget.getText()+'/'+str(slkp.sel_id))
				widget.set_tooltip_text(slkp.card_name.get_text())
				widget.redraw()
			slkp.destroy()
			pass
		pass
