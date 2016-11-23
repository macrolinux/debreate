# -*- coding: utf-8 -*-


import commands, wx

from dbr.buttons    import ButtonAdd
from dbr.buttons    import ButtonImport
from dbr.language   import GT
from dbr.pathctrl   import PATH_WARN
from dbr.pathctrl   import PathCtrl
from globals.ident  import ID_CHANGELOG


## TODO: Doxygen
class Panel(wx.ScrolledWindow):
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent, ID_CHANGELOG, name=GT(u'Changelog'))
        
        self.SetScrollbars(0, 20, 0, 0)
        
        self.package_text = wx.StaticText(self, -1, GT(u'Package'))
        self.package = wx.TextCtrl(self)
        
        tt_package = wx.ToolTip(GT(u'Name of the package/software'))
        self.package_text.SetToolTip(tt_package)
        self.package.SetToolTip(tt_package)
        
        self.version_text = wx.StaticText(self, -1, GT(u'Version'))
        self.version = wx.TextCtrl(self)
        
        tt_version = wx.ToolTip(GT(u'Package/Software release version'))
        self.version_text.SetToolTip(tt_version)
        self.version.SetToolTip(tt_version)
        
        self.distribution_text = wx.StaticText(self, -1, GT(u'Distribution'))
        self.distribution = wx.TextCtrl(self)
        
        tt_dist = wx.ToolTip(GT(u'Target distribution for Debian/Ubuntu'))
        self.distribution_text.SetToolTip(tt_dist)
        self.distribution.SetToolTip(tt_dist)
        
        self.urgency_text = wx.StaticText(self, -1, GT(u'Urgency'))
        self.urgency_opt = (u'low', u'HIGH')
        self.urgency = wx.Choice(self, choices=self.urgency_opt)
        self.urgency.SetSelection(0)
        
        tt_urgency = wx.ToolTip(GT(u'Urgency of this update'))
        self.urgency_text.SetToolTip(tt_urgency)
        self.urgency.SetToolTip(tt_urgency)
        
        self.maintainer_text = wx.StaticText(self, -1, GT(u'Maintainer'))
        self.maintainer = wx.TextCtrl(self)
        
        tt_maintaner = wx.ToolTip(GT(u'Package/Software maintainer\'s full name'))
        self.maintainer_text.SetToolTip(tt_maintaner)
        self.maintainer.SetToolTip(tt_maintaner)
        
        self.email_text = wx.StaticText(self, -1, GT(u'Email'))
        self.email = wx.TextCtrl(self)
        
        tt_email = wx.ToolTip(GT(u'Package/Software maintaner\'s email address'))
        self.email_text.SetToolTip(tt_email)
        self.email.SetToolTip(tt_email)
        
        info_sizer = wx.FlexGridSizer(2, 6, 5, 5)
        info_sizer.AddGrowableCol(1)
        info_sizer.AddGrowableCol(3)
        info_sizer.AddGrowableCol(5)
        info_sizer.AddMany([
            (self.package_text, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT), (self.package, 1, wx.EXPAND),
            (self.version_text, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT), (self.version, 1, wx.EXPAND),
            (self.distribution_text, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT), (self.distribution, 1, wx.EXPAND),
            (self.urgency_text, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT), (self.urgency, 1, wx.EXPAND),
            (self.maintainer_text, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT), (self.maintainer, 1, wx.EXPAND),
            (self.email_text, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT), (self.email, 1, wx.EXPAND)
            ])
        
        # *** CHANGES DETAILS
        self.changes = wx.TextCtrl(self, size=(20,150), style=wx.TE_MULTILINE)
        
        self.changes.SetToolTip(wx.ToolTip(GT(u'Enter one change per line')))
        
        self.border_changes = wx.StaticBox(self, -1, GT(u'Changes'), size=(20,20))
        changes_box = wx.StaticBoxSizer(self.border_changes, wx.VERTICAL)
        changes_box.Add(self.changes, 1, wx.EXPAND|wx.TOP|wx.BOTTOM, 5)
        
        # Destination of changelog
        self.rb_dest_default = wx.RadioButton(self, -1, u'/usr/share/doc/<package>', style=wx.RB_GROUP)
        self.rb_dest_custom = wx.RadioButton(self)
        self.dest_custom = PathCtrl(self, -1, u'/', PATH_WARN)
        
        self.rb_dest_default.SetToolTip(wx.ToolTip(GT(u'Install changelog to standard directory')))
        self.rb_dest_custom.SetToolTip(wx.ToolTip(GT(u'Install changelog to custom directory')))
        
        dest_custom_sizer = wx.BoxSizer(wx.HORIZONTAL)
        dest_custom_sizer.Add(self.rb_dest_custom)
        dest_custom_sizer.Add(self.dest_custom, 1)
        
        border_dest = wx.StaticBox(self, -1, GT(u'Target'))
        dest_box = wx.StaticBoxSizer(border_dest, wx.VERTICAL)
        dest_box.AddSpacer(5)
        dest_box.Add(self.rb_dest_default)
        dest_box.AddSpacer(5)
        dest_box.Add(dest_custom_sizer, 0, wx.EXPAND)
        dest_box.AddSpacer(5)
        
        details_sizer = wx.BoxSizer(wx.HORIZONTAL)
        details_sizer.Add(changes_box, 1, wx.EXPAND|wx.RIGHT, 5)
        details_sizer.Add(dest_box)
        
        
        self.button_import = ButtonImport(self)
        self.button_import.SetToolTip(wx.ToolTip(GT(u'Import information from Control page')))
        self.button_add = ButtonAdd(self)
        self.button_add.SetToolTip(wx.ToolTip(GT(u'Prepend above changes to changelog')))
        
        wx.EVT_BUTTON(self.button_import, -1, self.ImportInfo)
        wx.EVT_BUTTON(self.button_add, -1, self.AddInfo)
        
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.button_import)
        button_sizer.Add(self.button_add)
        
        self.display_area = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE)
        self.display_area.SetToolTip(wx.ToolTip(GT(u'Formatted changelog (editable)')))
        
        
        # *** LAYOUT
        main_sizer = wx.StaticBoxSizer(wx.StaticBox(self), wx.VERTICAL)
        main_sizer.AddSpacer(10)
        main_sizer.Add(info_sizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        main_sizer.AddSpacer(10)
        main_sizer.Add(details_sizer, 0, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        main_sizer.Add(button_sizer, 0, wx.LEFT|wx.RIGHT, 5)
        main_sizer.Add(self.display_area, 1, wx.EXPAND|wx.LEFT|wx.RIGHT, 5)
        main_sizer.AddSpacer(5)
        
        self.SetAutoLayout(True)
        self.SetSizer(main_sizer)
        self.Layout()
    
    
    ## TODO: Doxygen
    def ImportInfo(self, event):
        main_window = wx.GetApp().GetTopWindow()
        
        # Import package name and version from the control page
        self.package.SetValue(main_window.page_control.pack.GetValue())
        self.version.SetValue(main_window.page_control.ver.GetValue())
        self.maintainer.SetValue(main_window.page_control.auth.GetValue())
        self.email.SetValue(main_window.page_control.email.GetValue())
    
    
    ## TODO: Doxygen
    def AddInfo(self, event):
        package = self.package.GetValue()
        version = self.version.GetValue()
        distribution = self.distribution.GetValue()
        urgency = self.urgency_opt[self.urgency.GetSelection()]
        info1 = u'{} ({}) {}; urgency={}'.format(package, version, distribution, urgency)
        
        details = []
        for line in self.changes.GetValue().split(u'\n'):
            if line == self.changes.GetValue().split(u'\n')[0]:
                line = u'  * {}'.format(line)
            else:
                line = u'    {}'.format(line)
            details.append(line)
        details.insert(0, wx.EmptyString)
        details.append(wx.EmptyString)
        details = u'\n'.join(details)
        
        maintainer = self.maintainer.GetValue()
        email = self.email.GetValue()
        #date = commands.getoutput(u'date +"%a, %d %b %Y %T %z"')
        # A simpler way to get the date
        date = commands.getoutput(u'date -R')
        info2 = u' -- {} <{}>  {}'.format(maintainer, email, date)
        
        entry = u'\n'.join((info1, details, info2))
        self.display_area.SetValue(u'\n'.join((entry, wx.EmptyString, self.display_area.GetValue())))
    
    
    ## TODO: Doxygen.
    def GetChangelog(self):
        return self.display_area.GetValue()
    
    
    ## TODO: Doxygen
    def SetChangelog(self, data):
        changelog = data.split(u'\n')
        dest = changelog[0].split(u'<<DEST>>')[1].split(u'<</DEST>>')[0]
        if dest == u'DEFAULT':
            self.rb_dest_default.SetValue(True)
        else:
            self.rb_dest_custom.SetValue(True)
            self.dest_custom.SetValue(dest)
        self.display_area.SetValue(u'\n'.join(changelog[1:]))
        #self.Toggle(True)
    
#    def Toggle(self, value):
#        # Enable/Disable all fields
#        for item in self.toggle_list:
#            item.Enable(value)
    
    
    ## TODO: Doxygen
    def ResetAllFields(self):
        self.package.Clear()
        self.version.Clear()
        self.distribution.Clear()
        self.urgency.SetSelection(0)
        self.maintainer.Clear()
        self.email.Clear()
        self.changes.Clear()
        self.rb_dest_default.SetValue(True)
        self.dest_custom.SetValue(u'/')
        self.display_area.Clear()
    
    
    ## TODO: Doxygen
    def GatherData(self):
        if self.rb_dest_default.GetValue():
            dest = u'<<DEST>>DEFAULT<</DEST>>'
        elif self.rb_dest_custom.GetValue():
            dest = u'<<DEST>>' + self.dest_custom.GetValue() + u'<</DEST>>'
        
        return u'\n'.join((u'<<CHANGELOG>>', dest, self.display_area.GetValue(), u'<</CHANGELOG>>'))
