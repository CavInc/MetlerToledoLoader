#-*- coding:utf-8 -*-
import gtk

class LabelDesign(gtk.Frame):
	'''
	   Редактор этикеток
	'''
	
	def __get_separator(self):
		sep=gtk.SeparatorToolItem()
		return sep		
	
	def __set_toolbar(self):
		tb=gtk.Toolbar()
		tb.set_style(gtk.TOOLBAR_ICONS)
		insbutton=gtk.ToolButton(gtk.STOCK_NEW)
		insbutton.set_tooltip_text('Новая этикетка')
		openbutton=gtk.ToolButton(gtk.STOCK_OPEN)
		openbutton.set_tooltip_text('Открыть')
		savebutton=gtk.ToolButton(gtk.STOCK_SAVE)
		savebutton.set_tooltip_text('Сохранить')
		tb.insert(insbutton,0)
		tb.insert(openbutton,1)
		tb.insert(savebutton,2)
		tb.insert(self.__get_separator(),3)
		
		return tb
	
	def __set_value_list(self):
		s=['Название PLU','Назв. магазина','Дополн. тест','Рекламный текс','Текст даты','Дата','Время','Вес','Тара','Цена','Сумма','Фиксиров. вес','Цена до скидки','Ед. измерения','Номер','Штрих код','Спец. текст','Заголовок веса']
		model=gtk.ListStore(str)
		model.clear()
		for l in s:
			iter=model.append()
			model.set(iter,0,l)
		tree_v=gtk.TreeView(model)
		cell = gtk.CellRendererText()
		column = gtk.TreeViewColumn('Переменные', cell, text=0)
		tree_v.append_column(column)
		vb=gtk.ScrolledWindow()
		vb.add(tree_v)
		return vb
	def __set_draw(self):
		#vb=gtk.ScrolledWindow()
		tg=gtk.Table(2,2,False)
		hrule=gtk.HRuler()
		hrule.set_metric(gtk.PIXELS)
		hrule.set_range(7, 13, 0, 20)
		tg.attach(hrule,1,2,0,1,gtk.EXPAND|gtk.SHRINK|gtk.FILL, gtk.FILL, 0, 0)
		vrule=gtk.VRuler()
		vrule.set_metric(gtk.PIXELS)
		vrule.set_range(7,13,0,20)
		tg.attach(vrule,0,1,1,2, gtk.FILL, gtk.EXPAND|gtk.SHRINK|gtk.FILL, 0, 0)
		area = gtk.DrawingArea()
		tg.attach(area,1,2,1,2)
		
		#vb.add(tg)
		#return vb
		return tg
	def __set_parametr_panel(self):
		vbox=gtk.VBox()
		table=gtk.Table(4,2)
		table.attach(gtk.Label('Слева :'),0,1,0,1)
		self.lfpart=gtk.Entry()
		table.attach(self.lfpart,1,2,0,1)
		table.attach(gtk.Label('Сверху :'),0,1,1,2)
		self.tppart=gtk.Entry()
		table.attach(self.tppart,1,2,1,2)
		table.attach(gtk.Label('Ширина :'),0,1,2,3)
		self.width=gtk.Entry()
		table.attach(self.width,1,2,2,3)
		table.attach(gtk.Label('Высота :'),0,1,3,4)
		self.heigth=gtk.Entry()
		table.attach(self.heigth,1,2,3,4)
		fr=gtk.Frame()
		fr.add(table)
		vbox.pack_start(fr,False,True)
		fr=gtk.Frame()
		table=gtk.Table(2,2)
		table.attach(gtk.Label('Номер '),0,1,0,1)
		self.numbar=gtk.Entry()
		table.attach(self.numbar,1,2,0,1)
		fr.add(table)
		vbox.pack_start(fr,False,True)
		return vbox
		
	def __init__(self):
		gtk.Frame.__init__(self)
		self.set_label('Редактор этикеток')
		vbox=gtk.VBox()
		vbox.pack_start(self.__set_toolbar(),False,True,3)
		hbox=gtk.HBox(False)
		hbox.pack_start(self.__set_value_list(),False,True)
		hbox.pack_start(self.__set_draw(),True,True)
		hbox.pack_start(self.__set_parametr_panel(),False,True)
		vbox.pack_start(hbox,True,True)
		self.add(vbox)
		self.show_all()
		
