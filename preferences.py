import wx
import configobj

class PreferenceDialog(wx.Dialog):
	"""
	Creates and displays a preference dialog that allows the user to change
	some settings.
	"""

	def __init__(self):
		wx.Dialog.__init__(self,None,wx.ID_ANY,'Preferences',size=(500,300))
		self.createWidgets()

	def createWidgets(self):

		lblSizer = wx.BoxSizer(wx.VERTICAL)
		valueSizer = wx.BoxSizer(wx.VERTICAL)
		btnSizer = wx.StdDialogButtonSizer()
		colSizer = wx.BoxSizer(wx.HORIZONTAL)
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		iniFile = "config.ini"
		self.config = configobj.ConfigObj(iniFile);

		#labels = self.config.keys()
		labels = self.config["Labels"]
		values = self.config["Values"]
		self.widgetNames = values
		font = wx.Font(12,wx.SWISS,wx.NORMAL,wx.BOLD);

		for key in labels:
			value = labels[key] 
			lbl = wx.StaticText(self, label=value)
			lbl.SetFont(font)
			lblSizer.Add(lbl,0,wx.ALL,5)

		for key in values:
			value = values[key]
			if isinstance(value,list):
				default = value[0]
				choices = value[1:]
				cbo = wx.ComboBox(self,value=value[0],
								size=wx.DefaultSize,choices=choices,
								style=wx.CB_DROPDOWN|wx.CB_READONLY,
								name=key)
				valueSizer.Add(cbo,0,wx.ALL,5)
			else:
				txt = wx.TextCtrl(self,value=value,name=key)
				valueSizer.Add(txt,0,wx.ALL|wx.EXPAND,5)
				
		saveBtn = wx.Button(self,wx.ID_OK, label="Save")
		saveBtn.Bind(wx.EVT_BUTTON, self.onSave)
		btnSizer.AddButton(saveBtn)

		cancelBtn = wx.Button(self,wx.ID_CANCEL)
		btnSizer.AddButton(cancelBtn)
		btnSizer.Realize()

		colSizer.Add(lblSizer)
		colSizer.Add(valueSizer,1,wx.EXPAND)
		mainSizer.Add(colSizer,0,wx.EXPAND)
		mainSizer.Add(btnSizer,0,wx.ALL|wx.ALIGN_RIGHT,5)
		self.SetSizer(mainSizer)

	def onSave(self,event):
		for name in self.widgetNames:
			widget = wx.FindWindowByName(name)
			if isinstance(widget,wx.ComboBox):
				selection = widget.GetValue()
				choices = widget.GetItems()
				choices.insert(0,selection)
				self.widgetNames[name] = choices
			el:ese:
				value = widget.GetValue()
				self.widgetNames[name] = value
		self.config.write()
		self.EndModal(0)

class CheckListItem(wx.CheckListBox):

	def __init__(self,parent,id=-1,size=(250,300),choices=[]):
		wx.CheckListBox.__init__(self,parent,id,size,choices)
		
		

class MyApp(wx.App):
	def OnInit(self):
		dlg = PreferenceDialog()
		dlg.ShowModal()
		dlg.Destroy()

		return True

if __name__ == "__main__":
	app = MyApp(False)
	app.MainLoop()
