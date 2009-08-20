# -----
# clipboard
# -----
# by Reto Spoerri
# rspoerri AT nouser.org
# http://www.nouser.org
#
# Thanks to Laurens for testing & fixing under linux (kde/gnome)
#
# -----
# provides access to clipboard using different techniques
# for different platforms
# currently available:
# 
# -----

import os, sys
class applicationFinderClass:
  ''' check the PATH variable and store all application paths found
  for later usage '''
  def __init__( self ):
    self.foundApplications = dict()
    for rootPath in os.environ['PATH'].split(os.pathsep):
      dirFiles = os.listdir(rootPath)
      for aFile in dirFiles:
        filepath = os.path.join(rootPath, aFile)
        os.path.isfile(filepath)
        self.foundApplications[aFile] = filepath
  def __getitem__( self, filename ):
    if self.foundApplications.has_key( filename ):
      return self.foundApplications[filename]
    else:
      return None
applicationFinder = applicationFinderClass()


# platform specific imports
#import sys
clipboardClass = None
if sys.platform == 'darwin':
  import os
  
  if applicationFinder['pbcopy'] is not None \
  and applicationFinder['pbpaste'] is not None:
    class clipboardClass:
      def setText( self, pasteString ):
        # set a 
        cmd = os.popen(applicationFinder['pbcopy'], 'w')
        cmd.write(pasteString)
        cmd.close()
      def getText( self ):
        cmd = os.popen(applicationFinder['pbpaste'], 'r')
        out = cmd.read()
        cmd.close()
        return out
    print "I: using pbcopy/pbpaste clipboard"
  else:
    pass
  
elif sys.platform == 'win32':
  try:
    import win32clipboard as w 
    import win32con
    
    class clipboardClass:
      def setText(self, aString, aType=win32con.CF_TEXT): 
        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData( aType, aString ) 
        w.CloseClipboard()
      def getText( self ):
        w.OpenClipboard() 
        d=w.GetClipboardData(win32con.CF_TEXT) 
        w.CloseClipboard() 
        return d
    print "I: using win32clipboard"
  except:
    pass
  
elif sys.platform == 'linux2':
  import os
  
  # if one of the 'normal' clipboards work
  found = False
  
  try:
    # this has not been tested, especially the setText relies pure fantasy :)
    import pyqt
    class clipboardClass:
      def __init__( self ):
        # get the clipboard
        self.clipboard = QApplication.clipboard()
        
      def setText( self, pasteString ):
        # set the clipboard text data
        self.clipboard.setText( pasteString )
      
      def getText( self ):
        # read the clipboard text data.
        return self.clipboard.text()
    # test it
    self.clipboard.setText( self.clipboard.text() )
    # the clipboard seems to run correctly
    print "I: using pyqt clipboard"
    found = True
  except:
    pass
  
  try:
    import pydcop
    class clipboardClass:
      def __init__( self ):
        self.klipper = pydcop.DCOPObject("klipper", "klipper")
     
      def setText( self, pasteString ):
        self.klipper.setClipboardContents(pasteString)
     
      def getText( self ):
        return self.klipper.getClipboardContents()
    # Test if we really use KDE
    clipboardClass().getText()
    print "I: using pydcop clipboard"
    found = True
  except:
    pass
  
  try:
    import pygtk
    pygtk.require('2.0')
    import gtk
    
    class clipboardClass:
      def __init__( self ):
        # get the clipboard
        self.clipboard = gtk.clipboard_get()
        
      def setText( self, pasteString ):
        # set the clipboard text data
        self.clipboard.set_text(pasteString)
        # make our data available to other applications
        self.clipboard.store()
      
      def getText( self ):
        # read the clipboard text data. you can also read image and
        # rich text clipboard data with the
        # wait_for_image and wait_for_rich_text methods.
        return self.clipboard.wait_for_text()
    print "I: using pygtk/gtk clipboard"
    found = True
  except:
    pass
  
  xselPath = applicationFinder['xsel']
  xclipPath = applicationFinder['xclip']
  
  if found:
    pass
  elif xselPath is not None:
    class clipboardClass:
      def setText( self, pasteString ):
        # set a 
        cmd = os.popen(applicationFinder['xsel'], 'w')
        cmd.write(pasteString)
        cmd.close()
      def getText( self ):
        cmd = os.popen(applicationFinder['xsel'], 'r')
        out = cmd.read()
        cmd.close()
        return out
    print "I: using xsel clipboard"
  elif xclipPath is not None:
    class clipboardClass:
      def setText( self, pasteString ):
        # set a 
        cmd = os.popen(applicationFinder['xclip'], 'w')
        cmd.write(pasteString)
        cmd.close()
      def getText( self ):
        cmd = os.popen(applicationFinder['xclip'], 'r')
        out = cmd.read()
        cmd.close()
        return out
    print "I: using xclip clipboard"
  else:
    print "W: clipboard environment found!"


# if not clipboard could be created, use a dummy
if clipboardClass is None:
  print "ERROR: no clipboard module found for platform %s" % sys.platform
  print "  -  using dummy clipboard ( no interaction with os )"
  class clipboardClass:
    buffer = ''
    def setText( self, pasteString ):
      self.buffer = pasteString
    def getText( self ):
      return self.buffer


clipboard = clipboardClass()


if __name__ == '__main__':
  # execute the command and wait for the output
  print "platform   : '%s'" % sys.platform
  print "get        : '%s'" % clipboard.getText()
  text = 'hello world'
  clipboard.setText( text )
  print "set and get: '%s'" % clipboard.getText()
