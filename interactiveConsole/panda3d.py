# -----
# panda3dIOClass
# -----
# by Reto Spoerri
# rspoerri AT nouser.org
# http://www.nouser.org
# -----
# Creates a frame in a panda3d window, with a directEntry
# uses the clipboard class to copy, cut & paste
# output can be scrolled by page_up/down
# input can be scrolled by arrow_up/down
# -----



from shared import *

import textwrap, re, string, sys, os

from direct.gui.DirectGui import DirectFrame, DirectEntry, DirectLabel, DGG
from direct.showbase import DirectObject
from pandac.PandaModules import TextNode, Vec3, VBase4
from direct.gui.OnscreenText import OnscreenText

from clipboard import clipboard

class panda3dIOClass( DirectObject.DirectObject ):
  # set gui key to None if you want to call toggleConsole from outside this class
  gui_key = PANDA3D_CONSOLE_TOGGLE_KEY
  autocomplete_key = PANDA3D_CONSOLE_AUTOCOMPLETE_KEY
  autohelp_key = PANDA3d_CONSOLE_AUTOHELP_KEY
  # change size of text and number of characters on one line
  # scale of frame ( must be small (0.0x)
  scale = PANDA3D_CONSOLE_SCALE
  # to define a special font, if loading fails the default font is used (without warning)
  font = PANDA3D_CONSOLE_FONT
  fontWidth = PANDA3D_CONSOLE_FONT_WIDTH
  # frame position and size (vertical & horizontal)
  h_pos   = PANDA3D_CONSOLE_HORIZONTAL_POS
  h_size  = PANDA3D_CONSOLE_HORIZONTAL_SIZE
  # v_size + v_pos should not exceed 2.0, else parts of the interface will not be visible
  # space above the frame ( must be below 2.0, best between 0.0 and 1.0 )
  v_pos   = PANDA3D_CONSOLE_VERTICAL_POS
  # vertical size of the frame ( must be at max 2.0, best between 0.5 and 2.0 )
  v_size  = PANDA3D_CONSOLE_VERTICAL_SIZE
  linelength = int((h_size/scale - 5) / fontWidth)
  print "max number of characters on a length:", linelength
  numlines = int(v_size/scale - 5)
  defaultTextColor  = (0.0,0.0,0.0,1.0)
  autoCompleteColor = (0.9,0.9,0.9,1.0)
  def __init__( self, parent ):
    self.parent = parent
    
    # line wrapper
    self.linewrap = textwrap.TextWrapper()
    self.linewrap.width = self.linelength
    
    # calculate window size
    left   = (self.h_pos) / self.scale
    right  = (self.h_pos + self.h_size) / self.scale
    bottom = (self.v_pos) / self.scale
    top    = (self.v_pos + self.v_size) /self.scale
    
    # panda3d interface
    self.consoleFrame = DirectFrame ( relief = DGG.GROOVE
                                    , frameColor = (200, 200, 200, 0.5)
                                    , scale=self.scale
                                    , frameSize = (0, self.h_size / self.scale, 0, self.v_size / self.scale) )
    self.windowEvent( base.win )
    
    # try to load the defined font
    fixedWidthFont = loader.loadFont(self.font)
    # if font is not valid use default font
    if not fixedWidthFont.isValid():
      if self.font is None:
        print "pandaInteractiveConsole.py :: could not load the defined font %s" % str(self.font)
      fixedWidthFont = DGG.getDefaultFont()
    
    # text entry line
    self.consoleEntry = DirectEntry ( self.consoleFrame
                                    , text        = ""
                                    , command     = self.onEnterPress
                                    , width       = self.h_size/self.scale - 2
                                    , pos         = (1, 0, 1.5)
                                    , initialText = ""
                                    , numLines    = 1
                                    , focus       = 1
                                    , entryFont   = fixedWidthFont)
    
    # output lines
    self.consoleOutputList = list()
    for i in xrange( self.numlines ):
      label = OnscreenText( parent = self.consoleFrame
                          , text = ""
                          , pos = (1, -i+3+self.numlines)
                          , align=TextNode.ALeft
                          , mayChange=1
                          , scale=1.0
                          , fg = self.defaultTextColor )
      label.setFont( fixedWidthFont )
      self.consoleOutputList.append( label )
    
    # list of the last commands of the user
    self.userCommandList = list()
    self.userCommandListLength = 100
    for i in xrange(self.userCommandListLength):
      self.userCommandList.append('')
    self.userCommandPos = 0
    
    # buffer for data
    self.textBuffer = list()
    self.textBufferLength = 1000
    for i in xrange(self.textBufferLength):
      self.textBuffer.append(['', DEFAULT_COLOR])
    self.textBufferPos = self.textBufferLength-self.numlines
    
    # toggle the window at least once to activate the events
    self.toggleConsole()
    self.toggleConsole()
    
    self.help()
  
  def help( self ):
    # output some info text about this module
    infoTxt = """ ------ Panda3dConsole ------
- press F1 to toggle it on/off
- use the usual copy, cut & paste keys
- page_up    : scrolls up
- page_down  : scrolls down
- arrow_up   : previous command
- arrow_down : next command
- BUGS       : if you paste a to long text, the entry blocks
         FIX : use cut to remove the whole line"""
    #for line in infoTxt.split('\n'):
    #  self.write( line, color=DEFAULT_COLOR )
    return infoTxt
  
  # write a string to the panda3d console
  def write( self, printString, color=defaultTextColor ):
    # remove not printable characters (which can be input by console input)
    printString = re.sub( r'[^%s]' % re.escape(string.printable[:95]), "", printString)
    
    splitLines = self.linewrap.wrap(printString)
    for line in splitLines:
      self.textBuffer.append( [line, color] )
      self.textBuffer.pop(0)
    
    self.updateOutput()
  
  def updateOutput( self ):
    for lineNumber in xrange(self.numlines):
      lineText, color = self.textBuffer[lineNumber + self.textBufferPos]
      self.consoleOutputList[lineNumber].setText( lineText )
      self.consoleOutputList[lineNumber]['fg'] = color
  
  # toggle the gui console
  def toggleConsole( self ):
    self.consoleFrame.toggleVis()
    hidden = self.consoleFrame.isHidden()
    self.consoleEntry['focus'] != hidden
    if hidden:
      self.ignoreAll()
      self.accept( self.gui_key, self.toggleConsole )
    else:
      self.ignoreAll()
      self.accept( 'page_up', self.scroll, [-5] )
      self.accept( 'page_up-repeat', self.scroll, [-5] )
      self.accept( 'page_down', self.scroll, [5] )
      self.accept( 'page_down-repeat', self.scroll, [5] )
      self.accept( 'window-event', self.windowEvent)
      
      self.accept( 'arrow_up'  , self.scrollCmd, [ 1] )
      self.accept( 'arrow_down', self.scrollCmd, [-1] )
      
      self.accept( self.gui_key, self.toggleConsole )
      self.accept( self.autocomplete_key, self.autocomplete )
      self.accept( self.autohelp_key, self.autohelp )
      
      # accept v, c and x, where c & x copy's the whole console text
      #messenger.toggleVerbose()
      #for osx use ('meta')
      if sys.platform == 'darwin':
        self.accept( 'meta', self.unfocus )
        self.accept( 'meta-up', self.focus )
        self.accept( 'meta-c', self.copy )
        self.accept( 'meta-x', self.cut )
        self.accept( 'meta-v', self.paste )
      #for windows use ('control')
      if sys.platform == 'win32' or sys.platform == 'linux2':
        self.accept( 'control', self.unfocus )
        self.accept( 'control-up', self.focus )
        self.accept( 'control-c', self.copy )
        self.accept( 'control-x', self.cut )
        self.accept( 'control-v', self.paste )
  
  def autocomplete( self ):
    currentText = self.consoleEntry.get()
    currentPos = self.consoleEntry.guiItem.getCursorPosition()
    newText = self.parent.autocomplete( currentText, currentPos )
    if newText != currentText:
      self.consoleEntry.set( newText )
      self.consoleEntry.setCursorPosition( len(newText) )
  
  def autohelp( self ):
    currentText = self.consoleEntry.get()
    currentPos = self.consoleEntry.guiItem.getCursorPosition()
    self.parent.autohelp( currentText, currentPos )
  
  def focus( self ):
    self.consoleEntry['focus'] = 1
  
  def unfocus( self ):
    self.consoleEntry['focus'] = 0
  
  def copy( self ):
    copy = self.consoleEntry.get()
    clipboard.setText( copy )
  
  def paste( self ):
    oldCursorPos = self.consoleEntry.guiItem.getCursorPosition()
    clipboardText = clipboard.getText()
    
    # compose new text line
    oldText = self.consoleEntry.get()
    newText = oldText[0:oldCursorPos] + clipboardText + oldText[oldCursorPos:]
    
    clipboardTextLines = newText.split(os.linesep)
    
    for i in xrange( len(clipboardTextLines)-1 ):
      currentLine = clipboardTextLines[i]
      # we only want printable characters
      currentLine = re.sub( r'[^' + re.escape(string.printable[:95]) + ']', "", currentLine)
      
      # set new text and position
      self.consoleEntry.set( currentLine )
      self.onEnterPress( currentLine )
    currentLine = clipboardTextLines[-1]
    currentLine = re.sub( r'[^' + re.escape(string.printable[:95]) + ']', "", currentLine)
    self.consoleEntry.set( currentLine )
    self.consoleEntry.setCursorPosition( len(self.consoleEntry.get()) )
    self.focus()
  
  def cut( self ):
    clipboard.setText( self.consoleEntry.get() )
    self.consoleEntry.enterText('')
    self.focus()
  
  def scroll( self, step ):
    self.textBufferPos += step
    self.textBufferPos = min( self.textBufferLength-self.numlines, max( 0, self.textBufferPos ) )
    self.updateOutput()
  
  def scrollCmd( self, step ):
    oldCmdPos = self.userCommandPos
    self.userCommandPos += step
    self.userCommandPos = min( self.userCommandListLength-1, max( 0, self.userCommandPos ) )
    self.userCommandList[oldCmdPos] = self.consoleEntry.get()
    newCmd = self.userCommandList[self.userCommandPos]
    self.consoleEntry.set( newCmd )
    self.consoleEntry.setCursorPosition( len(newCmd) )
  
  def onEnterPress( self, textEntered ):
    # set to last message
    self.textBufferPos = self.textBufferLength-self.numlines
    # clear line
    self.consoleEntry.enterText('')
    self.focus()
    # add text entered to user command list & remove oldest entry
    self.userCommandList.insert( 1, textEntered )
    self.userCommandList[0] = ''
    self.userCommandList.pop( -1 )
    self.userCommandPos = 0
    # call our parent
    self.parent.push( textEntered )
  
  def windowEvent( self, window ):
    """
    This is a special callback.
    It is called when the panda window is modified.
    """
    wp = window.getProperties()
    width = wp.getXSize() / float(wp.getYSize())
    height = wp.getYSize() / float(wp.getXSize())
    if width > height:
      height = 1.0
    else:
      width = 1.0
    # aligned to center
    consolePos = Vec3(-self.h_size/2, 0, -self.v_size/2)
    # aligned to left bottom
    #consolePos = Vec3(-width+self.h_pos, 0, -height+self.v_pos)
    # aligned to right top
    #consolePos = Vec3(width-self.h_size, 0, height-self.v_size)
    # set position
    self.consoleFrame.setPos( consolePos )
