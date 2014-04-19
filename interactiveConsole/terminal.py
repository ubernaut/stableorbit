# -----
# irc
# -----
# by Reto Spoerri
# rspoerri AT nouser.org
# http://www.nouser.org
# -----
# provides a console input
# -----


from shared import *

import sys, re, string

if sys.platform == 'win32':
  import msvcrt
elif sys.platform == 'linux2' or sys.platform == 'darwin':
  import termios, fcntl, os, select

from direct.task import Task

class consoleIOClass:
  def __init__( self, parent ):
    self.parent = parent
    # buffer of current text
    self.linebuffer = ''
    self.linebufferPos = 0
    # on linux and osx platforms we need to set the keyreading non blocking
    success = False
    if sys.platform == 'linux2' or sys.platform == 'darwin':
      try:
        # set read non blocking
        self.fd = sys.stdin.fileno()
        self.oldterm = termios.tcgetattr(self.fd)
        newattr = self.oldterm[:] #termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(self.fd, termios.TCSANOW, newattr)
        self.oldflags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)
        success = True
      except:
        print "D: interactiveConsole.consoleKeyreaderClass.__init__ cannot set reading non-blocking, skipping console mode\n"
    else:
      success = True
    
    if success:
      if DEBUG:
        print "D: interactiveConsole.consoleKeyreaderClass.__init__\n"
      # task to read the command line input
      if TERMINAL_TASK_TIME is None:
        taskMgr.add(self.read, 'pandaInteractiveConsoleReadtask')
      else:
        taskMgr.doMethodLater(TERMINAL_TASK_TIME, self.read, 'pandaInteractiveConsoleReadtask')
      
      # __del__ doesnt seem to be called all the times
      # so we make this at exit so the console works correctly afterwards
      import atexit
      atexit.register( self.resetConsole )
      
      self.help()
  
  def help( self ):
    return """ ------ commandlineConsole ------
- enter the text to execute
- backspace kind of works"""
  
  def resetConsole( self ):
    # reset settings of command console
    if sys.platform == 'linux2' or sys.platform == 'darwin':
      termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.oldterm)
      fcntl.fcntl(self.fd, fcntl.F_SETFL, self.oldflags)
  
  def readKey( self ):
    ''' read a single keypress from command line,
    on special key multiple reads are required '''
    # read key from keyboard
    char = None
    if sys.platform == 'win32':
      if msvcrt.kbhit():
        char = msvcrt.getch()
    elif sys.platform == 'linux2' or sys.platform == 'darwin':
      try:
        char = sys.stdin.read(1)
      except IOError: pass
    return char  
  
  # clear the line of the command console, (reqired for backspaces)
  def refreshLine( self ):
    # clear complete line
    for i in xrange(len(self.linebuffer)):
      sys.stdout.write("\b")
    # write it again
    self.parent.write( self.linebuffer+" " )
    sys.stdout.write("\b")

  # clear the line of the command console, (reqired for backspaces)
  def clearLine( self ):
    lineLen = len(self.linebuffer)
    # clear complete line
    for i in xrange(lineLen):
      sys.stdout.write("\b")
    for i in xrange(lineLen):
      sys.stdout.write(" ")
    for i in xrange(lineLen):
      sys.stdout.write("\b")
  
  def read( self, task ):
    # get keypress
    char = self.readKey()
    while char is not None:
      # execute command on carriage return (13 on windows / 10 on linux ???)
      if ord(char) == 13 or ord(char) == 10:
        self.clearLine()
        self.parent.push( self.linebuffer )
        self.linebuffer = ''
        self.linebufferPos = 0
      # clear last character on backspace
      elif ord(char) == 8 or ord(char) == 127:
        # remove the character from the console line
        sys.stdout.write("\b \b")
        # change the linebuffer
        self.linebuffer = self.linebuffer[0:self.linebufferPos-1] + self.linebuffer[self.linebufferPos:len(self.linebuffer)]
        self.linebufferPos = max(0, self.linebufferPos - 1)
        '''
      # move cursor to edit commandline
      # NOT TESTED, MAY WORK
      elif ord(char) == 224 or ord(char) == 1: # ord(char) == 27
        if sys.platform == 'linux2' or sys.platform == 'darwin':
          cmdKey = self.readKey()
        cmdKey = self.readKey()
        if ord(cmdKey) == 75 or ord(cmdKey) == 68:
          self.linebufferPos = max( 0, min( len(self.linebuffer), self.linebufferPos - 1 ) )
        elif ord(cmdKey) == 77 or ord(cmdKey) == 67:
          self.linebufferPos = max( 0, min( len(self.linebuffer), self.linebufferPos + 1 ) )
      '''
      # all other keypresses are added to the command line
      else:
        self.linebuffer = self.linebuffer[0:self.linebufferPos] + char + self.linebuffer[self.linebufferPos:len(self.linebuffer)]
        if self.linebufferPos+1 != len(self.linebuffer):
          diffLen = len(self.linebuffer) - self.linebufferPos+1
          self.refreshLine()
        else:
          sys.stdout.write(char)
        self.linebufferPos += 1
      # get keypress
      char = self.readKey() 
    return Task.cont
