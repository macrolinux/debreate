# -*- coding: utf-8 -*-

## \package input.pathctrl

# MIT licensing
# See: docs/LICENSE.txt


import os, wx

from input.essential    import EssentialField
from input.text         import TextArea


PATH_DEFAULT = wx.NewId()
PATH_WARN = wx.NewId()


## TODO: Doxygen
#  
#  FIXME: Use boolean value instead of type
class PathCtrl(TextArea):
    def __init__(self, parent, ctrl_id=wx.ID_ANY, value=u'/', defaultValue=u'/', ctrl_type=PATH_DEFAULT,
            default=wx.EmptyString, name=wx.TextCtrlNameStr):
        
        TextArea.__init__(self, parent, ctrl_id, value, defaultValue, name=name)
        
        self.ctrl_type = ctrl_type
        
        # Get the value of the textctrl so it can be restored
        self.default = default
        
        # For restoring color of text area
        self.clr_default = self.GetBackgroundColour()
        
        # Make sure first character is forward slash
        wx.EVT_KEY_UP(self, self.OnKeyUp)
        
        # Check if path is available on construction
        if self.ctrl_type == PATH_WARN:
            self.SetPathAvailable()
    
    
    ## TODO: Doxygen
    def GetDefaultValue(self):
        return self.default
    
    
    ## TODO: Doxygen
    def OnKeyUp(self, event=None):
        value = self.GetValue()
        insertion_point = self.GetInsertionPoint()+1
        if value == wx.EmptyString or value[0] != u'/':
            self.SetValue(u'/{}'.format(value))
            self.SetInsertionPoint(insertion_point)
        
        # If PathCtrl is set to warn on non-existent paths, change background color to red when path
        # doesn't exist
        value = self.GetValue()
        if self.ctrl_type == PATH_WARN:
            self.SetPathAvailable()
        
        if event:
            event.Skip()
    
    
    ## Resets text area to default value
    #  
    #  \override input.text.TextArea.Reset
    def Reset(self):
        TextArea.Reset(self)
        
        if self.ctrl_type == PATH_WARN:
            self.SetPathAvailable()
        
        self.SetInsertionPointEnd()
    
    
    ## TODO: Doxygen
    def SetPathAvailable(self):
        if os.path.isdir(self.GetValue()):
            self.SetBackgroundColour(self.clr_default)
            return
        
        self.SetBackgroundColour(u'red')
    
    
    ## TODO: Doxygen
    def SetDefaultValue(self, default):
        self.default = default


## TODO: Doxygen
class PathCtrlESS(PathCtrl, EssentialField):
    def __init__(self, parent, ctrl_id=wx.ID_ANY, value=wx.EmptyString, ctrl_type=PATH_DEFAULT,
            default=wx.EmptyString, name=wx.TextCtrlNameStr):
        
        PathCtrl.__init__(self, parent, ctrl_id, value, ctrl_type, default, name)
        EssentialField.__init__(self)
