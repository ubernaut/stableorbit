# -----
# testApp
# -----
# by Reto Spoerri
# rspoerri AT nouser.org
# http://www.nouser.org
# -----
# a litte framework for the panda console
# handles input output
# enables the different components
# -----

from shared import *

from terminal import consoleIOClass
from panda3d import panda3dIOClass
from irc import ircClientClass
from console import customConsoleClass

import sys, traceback

class pandaConsole:
  def __init__( self, interfaces=INPUT_GUI|INPUT_CONSOLE|OUTPUT_PYTHON|OUTPUT_IRC, localsEnv=globals ):
    self.guiEnabled     = (interfaces & INPUT_GUI)
    self.consoleEnabled = (interfaces & INPUT_CONSOLE)
    self.pythonEnabled  = (interfaces & OUTPUT_PYTHON)
    self.ircEnabled     = (interfaces & OUTPUT_IRC)
    
    if self.guiEnabled:
      self.panda3dConsole = panda3dIOClass( self )
    if self.consoleEnabled:
      self.terminalConsole = consoleIOClass( self )
    
    if self.pythonEnabled:
      self.customInteractiveConsole = customConsoleClass( localsEnv )
    if self.ircEnabled:
      self.ircClient = ircClientClass( self.echo )
    
    self.printHelp()
  
  def help( self ):
    return """ ------ Credits ------
By Reto Spoerri
rspoerri AT nouser.org
http://www.nouser.org/
free to use and change by anyone
 ------ HELP ------
enter %s to view this message again
 ------ have fun ------ """ % HELP_COMMAND
  
  def echo( self, output, pre='* ', color=(0,0,0,1) ):
    # output on panda3d interface
    if self.guiEnabled:
      for line in output.split('\n'):
        if len(line) > 0:
          self.panda3dConsole.write( "%s%s" % (pre, line), color )
    
    # output on commandline
    if self.consoleEnabled:
      for line in output.split('\n'):
        if len(line) > 0:
          print "%s%s" % (pre, line)
          # can possibly fail
          try:    sys.stdout.flush()
          except: pass
  
  def isIrc( self, input ):
    ircInput = None
    if self.ircEnabled:
      if len(input) > 0:
        if (IRC_PRE is None) and not (IRC_PRE_EXCLUDE != input[0]):
          ircInput = input[:]
        if (IRC_PRE == input[0]):
          ircInput = input[1:]
      else:
        if (IRC_PRE is None):
          ircInput = input[:]
    return ircInput
  
  def makeIrc( self, line ):
    if IRC_PRE is None:
      return line
    else:
      return "%s%s" % (IRC_PRE, line)
  
  def isPython( self, input ):
    consoleInput = None
    if self.pythonEnabled:
      if len(input) > 0:
        if (PYTHON_PRE is None) and (PYTHON_PRE_EXCLUDE != input[0]):
          consoleInput = input[:]
        if (PYTHON_PRE == input[0]):
          consoleInput = input[1:]
      else:
        if (PYTHON_PRE is None):
          consoleInput = input[:]
    return consoleInput
  
  def makePython( self, line ):
    if PYTHON_PRE is None:
      return line
    else:
      return "%s%s" % (PYTHON_PRE, line)
  
  def printHelp( self ):
    if self.guiEnabled:
      self.echo( self.panda3dConsole.help() )
    if self.consoleEnabled:
      self.echo( self.terminalConsole.help() )
    if self.pythonEnabled:
      self.echo( self.customInteractiveConsole.help() )
    if self.ircEnabled:
      self.echo( self.ircClient.help() )
    self.echo( self.help() )
  
  def autohelp( self, currentText, currentCursorPos ):
    if currentText == '':
      # if no text written -> output generic help
      self.printHelp()
    else:
      # remove any textcomponent signalling it as python code
      pythonText = self.isPython( currentText )
      # if this is python code
      if pythonText is not None:
        helpText = self.customInteractiveConsole.autohelp( pythonText, currentCursorPos )
        self.echo( helpText, '?> ', HELP_INFOTEXT_COLOR )
      
      # autohelp for irc not implemented
      ircText = self.isIrc( currentText )
      if ircText is not None:
        helpText = self.ircClient.autohelp( pythonText, currentCursorPos )
        self.echo( helpText, '?> ', HELP_INFOTEXT_COLOR )
  
  def autocomplete( self, currentText, currentCursorPos ):
    try:
      # remove the pre if the is python code
      pythonText = self.isPython( currentText )
      if pythonText is not None:
        newText, infoText = self.customInteractiveConsole.autocomplete( pythonText, currentCursorPos )
        newText = self.makePython( newText )
      
      # remove the pre if the is irc code
      ircText = self.isIrc( currentText )
      if ircText is not None:
        newText, infoText = self.ircClient.autocomplete( ircText, currentCursorPos )
        newText = self.makeIrc( newText )
      
      # output infoText
      if infoText is not None:
        self.echo( infoText, '* ', AUTOCOMPLETER_INFOTEXT_COLOR )
      
      return newText
    except:
      errorText = "ERROR in autocompletion:\n- %s\n- %s\n- %s\n" % \
                    ( str(sys.exc_info()[0])
                    , str(sys.exc_info()[1])
                    , '\n'.join(traceback.format_tb(sys.exc_info()[2], 10) ) )
      self.echo( errorText )
    return currentText
  
  def push( self, input ):
    # check if to be threaded as irc message
    ircInput = self.isIrc( input )
    # check if to be threaded as python command
    consoleInput = self.isPython( input )
    
    # call the interactive console
    if consoleInput is not None:
      outputLines = self.customInteractiveConsole.push( consoleInput )
      for text, pre, color in outputLines:
        self.echo( text, pre, color )
    # call the irc client
    if ircInput is not None:
      outputLines = self.ircClient.push( ircInput )
      for text, pre, color in outputLines:
        self.echo( text, pre, color )
  
  def toggle( self ):
    if self.guiEnabled:
      self.panda3dConsole.toggleConsole()