# -*- coding: utf-8 -*-

## \package ui.notebook

# MIT licensing
# See: docs/LICENSE.txt


import wx
from wx.aui import AUI_NB_CLOSE_ON_ACTIVE_TAB
from wx.aui import AUI_NB_SCROLL_BUTTONS
from wx.aui import AUI_NB_TAB_MOVE
from wx.aui import AUI_NB_TAB_SPLIT
from wx.aui import AUI_NB_TOP
from wx.aui import AuiNotebook
from wx.aui import EVT_AUINOTEBOOK_PAGE_CLOSE

from dbr.containers         import Contains
from dbr.language           import GT
from dbr.log                import Logger
from globals.strings        import TextIsEmpty
from globals.wizardhelper   import GetMainWindow
from input.toggle           import CheckBox
from ui.button              import ButtonAdd
from ui.dialog              import ShowDialog
from ui.dialog              import ShowErrorDialog
from ui.layout              import BoxSizer
from ui.panel               import ScrolledPanel
from ui.prompt              import TextEntryDialog


# ???: What is TAB_SPLIT for?
DEFAULT_NB_STYLE = AUI_NB_TOP|AUI_NB_TAB_SPLIT|AUI_NB_TAB_MOVE|AUI_NB_CLOSE_ON_ACTIVE_TAB|AUI_NB_SCROLL_BUTTONS


## Custom notebook class for compatibility with legacy wx versions
class Notebook(AuiNotebook):
    def __init__(self, parent, win_id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize,
            style=DEFAULT_NB_STYLE, name=u'notebook'):
        
        AuiNotebook.__init__(self, parent, win_id, pos, size, style)
        
        # wx.aui.AuiNotebook does not allow setting name from constructor
        self.Name = name
    
    
    ## Adds a new page
    #  
    #  \param caption
    #    Label displayed on tab
    #  \param page
    #    \b \e wx.Window instance that will be new page (if None, a new instance is created)
    #  \param select
    #    Specifies whether the page should be selected
    #  \param bitmap:
    #    Specifies optional image
    def AddPage(self, caption, page=None, win_id=wx.ID_ANY, select=False, imageId=0):
        if not page:
            page = wx.Panel(self, win_id)
        
        # Existing instance should already have an ID
        elif win_id != wx.ID_ANY:
            Logger.Warn(__name__, u'Option "win_id" is only used if "page" is None')
        
        if wx.MAJOR_VERSION <= 2:
            if not isinstance(imageId, wx.Bitmap):
                imageId = wx.NullBitmap
        
        AuiNotebook.AddPage(self, page, caption, select, imageId)
        
        return page
    
    
    ## Adds a ui.panel.ScrolledPanel instance as new page
    #  
    #  \param caption
    #    Label displayed on tab
    #  \param select
    #    Specifies whether the page should be selected
    #  \param bitmap:
    #    Specifies optional image
    def AddScrolledPage(self, caption, win_id=wx.ID_ANY, select=False, imageId=0):
        return self.AddPage(caption, ScrolledPanel(self), win_id, select, imageId)
    
    
    ## Deletes all pages
    #  
    #  \override wx.aui.AuiNotebook.DeleteAllPages
    def DeleteAllPages(self):
        if wx.MAJOR_VERSION > 2:
            return AuiNotebook.DeleteAllPages(self)
        
        # Reversing only used for deleting pages from right to left (not necessary)
        for INDEX in reversed(range(self.GetPageCount())):
            self.DeletePage(INDEX)


## Multiple instances of a single template
#  
#  \param parent
#    \b \e wx.Window parent instance
#  \param panelClass
#    \b \e wx.Window derived class to use for tab pages
class TabsTemplate(BoxSizer):
    def __init__(self, parent, panelClass):
        BoxSizer.__init__(self, wx.VERTICAL)
        
        self.Panel = panelClass
        
        btn_add = ButtonAdd(parent)
        txt_add = wx.StaticText(parent, label=GT(u'Add page'))
        
        self.Tabs = Notebook(parent)
        
        # *** Event Handling *** #
        
        btn_add.Bind(wx.EVT_BUTTON, self.OnButtonAdd)
        
        self.Tabs.Bind(EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnCloseTab)
        
        # *** Layout *** #
        
        lyt_add = wx.BoxSizer(wx.HORIZONTAL)
        lyt_add.Add(btn_add)
        lyt_add.Add(txt_add, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5)
        
        self.Add(lyt_add, 0, wx.EXPAND|wx.ALL, 5)
        self.Add(self.Tabs, 1, wx.ALL|wx.EXPAND, 5)
    
    
    ## Check if name is okay for page filename
    def _name_is_ok(self, name):
        if TextIsEmpty(name):
            return False
        
        return not Contains(name, (u' ', u'\t',))
    
    
    ## Adds a new page to the Notebook instance
    def AddPage(self, title, select=True):
        new_page = self.Panel(self.GetParent(), name=title)
        
        return self.Tabs.AddPage(title, new_page, select)
    
    
    ## Retrieves parent window
    def GetParent(self):
        return self.Tabs.Parent
    
    
    ## TODO: Doxygen
    def OnButtonAdd(self, event=None):
        if event:
            event.Skip(True)
        
        return self.SetPageName()
        #return self.AddPage(u'test')
    
    
    ## TODO: Doxygen
    def OnCloseTab(self, event=None):
        Logger.Debug(__name__, u'Closing tab')
    
    
    ## Change tab name & filename
    def OnRenamePage(self, event=None):
        index = self.Tabs.GetSelection()
        
        return self.SetPageName(index, rename=True)
    
    
    ## Either renames an existing page or creates a new one
    #  
    #  \param index
    #    Page index to rename (only used if 'rename' is True)
    #  \param rename
    #    Renames an existing page instead of creating a new one
    def SetPageName(self, index=-1, rename=False):
        getname = TextEntryDialog(GetMainWindow(), GT(u'Name for new page'))
        new_name = None
        
        if not rename:
            easy_mode = CheckBox(getname, label=u'Easy mode')
            easy_mode.SetValue(True)
            
            sizer = getname.GetSizer()
            insert_point = len(sizer.GetChildren()) - 1
            
            sizer.InsertSpacer(insert_point, 5)
            sizer.Insert(insert_point + 1, easy_mode, 0, wx.LEFT, 16)
            
            getname.SetSize(sizer.GetMinSize())
            getname.Fit()
            getname.CenterOnParent()
        
        valid_name = False
        
        while not valid_name:
            if new_name and TextIsEmpty(new_name):
                getname.Clear()
            
            # User cancelled
            if not ShowDialog(getname):
                return False
            
            else:
                new_name = getname.GetValue()
            
            valid_name = self._name_is_ok(new_name)
            
            if valid_name:
                break
            
            ShowErrorDialog(GT(u'Page name cannot contain whitespace'), warn=True)
        
        if rename:
            if index < 0:
                return False
            
            return self.Tabs.SetPageText(index, new_name)
        
        return self.AddPage(new_name, easy_mode.GetValue())
