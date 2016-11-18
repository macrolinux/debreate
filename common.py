# -*- coding: utf-8 -*-


import os, subprocess, sys, wx

from dbr.language import GT


maj_pyversion = sys.version_info[0]
mid_pyversion = sys.version_info[1]
min_pyversion = sys.version_info[2]
python_version = u'{}.{}.{}'.format(maj_pyversion, mid_pyversion, min_pyversion)



##################
###     FUNCTIONS       ###
##################

def RequirePython(version):
    error = u'Incompatible python version'
    t = type(version)
    if t == type(u''):
        if version == python_version[0:3]:
            return
        raise ValueError(error)
    elif t == type([]) or t == type(()):
        if python_version[0:3] in version:
            return
        raise ValueError(error)
    raise ValueError(u'Wrong type for argument 1 of RequirePython(version)')


### -*- Function to check for installed executables -*- ###
def CommandExists(command):
    try:
        subprocess.Popen(command.split(u' ')[0].split(u' '))
        exists = True
        print u'First subprocess: {}'.format(exists)
    except OSError:
        exists = os.path.isfile(command)
        print u'os.path: {}'.format(exists)
        if exists:
            subprocess.Popen((command))
            print u'Second subprocess: {}'.format(exists)
    return exists


ID_APPEND = wx.NewId()
ID_OVERWRITE = wx.NewId()


### -*- Dialog for overwrite prompt of a text area -*- ###
class OverwriteDialog(wx.Dialog):
    def __init__(self, parent, id=-1, title=GT(u'Overwrite?'), message=u''):
        wx.Dialog.__init__(self, parent, id, title)
        self.message = wx.StaticText(self, -1, message)
        
        self.button_overwrite = wx.Button(self, ID_OVERWRITE, GT(u'Overwrite'))
        self.button_append = wx.Button(self, ID_APPEND, GT(u'Append'))
        self.button_cancel = wx.Button(self, wx.ID_CANCEL)
        
        ### -*- Button events -*- ###
        wx.EVT_BUTTON(self.button_overwrite, ID_OVERWRITE, self.OnButton)
        wx.EVT_BUTTON(self.button_append, ID_APPEND, self.OnButton)
        
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.button_overwrite, 0, wx.LEFT|wx.RIGHT, 5)
        hsizer.Add(self.button_append, 0, wx.LEFT|wx.RIGHT, 5)
        hsizer.Add(self.button_cancel, 0, wx.LEFT|wx.RIGHT, 5)
        
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.message, 1, wx.ALIGN_CENTER|wx.ALL, 5)
        vsizer.Add(hsizer, 0, wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM, 5)
        
        self.SetAutoLayout(True)
        self.SetSizerAndFit(vsizer)
        self.Layout()
    
    def OnButton(self, event):
        id = event.GetEventObject().GetId()
        self.EndModal(id)
    
    def GetMessage(self, event=None):
        return self.message.GetLabel()


### -*- Object for Dropping Text Files -*-
class SingleFileTextDropTarget(wx.FileDropTarget):
    def __init__(self, obj):
        wx.FileDropTarget.__init__(self)
        self.obj = obj
    
    def OnDropFiles(self, x, y, filenames):
        if len(filenames) > 1:
            raise StandardError(GT(u'Too many files'))
        text = open(filenames[0]).read()
        try:
            if (not TextIsEmpty(self.obj.GetValue())):
                overwrite = OverwriteDialog(self.obj, message = GT(u'The text area is not empty!'))
                id = overwrite.ShowModal()
                if (id == ID_OVERWRITE):
                    self.obj.SetValue(text)
                elif (id == ID_APPEND):
                    self.obj.SetInsertionPoint(-1)
                    self.obj.WriteText(text)
            else:
                self.obj.SetValue(text)
        except UnicodeDecodeError:
            wx.MessageDialog(None, GT(u'Error decoding file'), GT(u'Error'), wx.OK).ShowModal()


### -*- Checks if Text Control is Empty -*- ###
def TextIsEmpty(text):
    text = u''.join(u''.join(text.split(u' ')).split(u'\n'))
    return (text == u'')