# -----
# irc
# -----
# by Reto Spoerri
# rspoerri AT nouser.org
# http://www.nouser.org
# -----
# provides basic support for a irc client connection
# -----

from shared import *
from completer import completeIrcCommand

from direct.task import Task
import socket, sys, time, re, traceback

class ircClientClass:
  defaultColor      = (0.0,0.0,0.0,1.0)
  svrmsgColor       = (0.8,0.8,1.0,1.0)
  chanmsgColor      = svrmsgColor
  genmsgColor       = svrmsgColor
  connectmsgColor   = (0.5,0.1,0.5,1.0)
  disconnectColor   = connectmsgColor
  joinmsgColor      = (0.5,0.2,0.2,1.0)
  nickmsgColor      = joinmsgColor
  partmsgColor      = joinmsgColor
  messageColor      = (0.2,0.2,0.2,1.0)
  prvmsgColor       = messageColor
  exceptionColor    = (1.0,0.0,0.0,1.0)
  unhandledmsgColor = exceptionColor
  def __init__( self, outputCallBack ):
    self.outputCallBack = outputCallBack
    
    self.server = None
    self.port = None
    self.nick = ''
    self.realname = ''
    self.channel = ""
    self.usercmd = re.compile('^/(\w+)( (.*))?$')
    self.usermsg = self.svrmsg = self.chanmsg = None
    self.genmsg = self.pingmsg = self.infomsg = None
    self.sock = None
    
    self.help()
  
  def help( self ):
    text = ''
    text += " ------ IRC ------ \n"
    if IRC_PRE is None:
      text += """- direct entry enabled\n"""
    else:
      text += """- use '%s' in front of a line to send it to the irc component
- example: %s/connect irc.freenode.net 6667 username real name
- example: %syourmessage to the connected channel
TAB      : autocomplete commands""" % (IRC_PRE,IRC_PRE,IRC_PRE)
    return text
  
  def connect(self, parameters ): #svr="irc.freenode.net", prt=6667, nck="PythIRC", rname="Python-IRC User"):
    # if already connected
    if self.sock is not None:
      self.disconnect()
    
    parametersList = parameters.split(' ')
    self.server = parametersList[0]
    self.port = int( parametersList[1] )
    self.nick = parametersList[2]
    self.realname = "".join(parametersList[2:])
    
    self.outputCallBack( "CONNECTING TO %s:%i as %s (%s) " % (self.server, self.port, self.nick, self.realname), '# ', self.connectmsgColor )
    
    self.usercmd = re.compile('^/(\w+)( (.*))?$')
    self.usermsg = re.compile('^(#?\w+)( (.*))?$')
    self.svrmsg  = re.compile('^:([a-zA-Z0-9\.-]+) [0-9]+ %s (.*)' % self.nick)
    self.chanmsg = re.compile('^:(.+)![~]?(.+)@(.+) (\w+) #?(\w+) :(.*)$')
    self.genmsg  = re.compile('^:(.+)!~?(.+)@([a-zA-Z0-9\-\.]+) (\w+) :?(.*)$')
    self.pingmsg = re.compile('^PING :(.*)$', re.IGNORECASE)
    self.pongmsg = re.compile('^:([a-zA-Z0-9\.-]+) PONG ([a-zA-Z0-9\.-]+) :([a-zA-Z0-9\.-]+)$', re.IGNORECASE)
    
    # connect to the IRC server.
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((self.server, self.port))
    self.sock.setblocking(0)
    self.sock.settimeout(0)
    # set default parameters
    nickcmd = "NICK %s\n" % self.nick
    self.sock.sendall(nickcmd)
    usercmd = "USER Python-IRC host server : %s\n" % self.realname
    self.sock.sendall(usercmd)
    
    # task to read the command line input
    if IRC_TASK_TIME is None:
      taskMgr.add(self.fetchNetworkData, 'fetchNetworkData')
    else:
      taskMgr.doMethodLater(IRC_TASK_TIME, self.fetchNetworkData, 'fetchNetworkData')
    self.lastPingTime = 0.0
  
  def disconnect( self ):
    taskMgr.remove('fetchNetworkData')
    if self.sock:
      self.sock.close()
      self.sock = None
  
  def push( self, input ):
    sendData, color = self.parsecmd(input)
    self.send( sendData + "\n" )
    return [sendData, '# ', color],
    #self.outputCallBack( sendData, '#', color )
  
  def send( self, msg ):
    try:    self.sock.sendall(msg)
    except: pass
  
  def receive( self ):
    data = ''
    try:    data = self.sock.recv(8192)
    except: pass
    return data
  
  def fetchNetworkData(self, task):
    dataJunk = self.receive()
    for lineJunk in dataJunk.split('\n'):
      line, color = self.parseinput( lineJunk.strip() )
      if len(line) > 0:
        self.outputCallBack( line, '#', color )
      else :
        # No data from socket - socket may be closed
        # Test this and exit gracefully if needed
        try :
          # send a ping every 30 seconds
          if task.time - self.lastPingTime > 30.0:
            self.send("PING %s\n" % self.server)
            self.lastPingTime = task.time
        except socket.error :
          self.disconnect()
          print "Socket closed by host."
          return Task.done
    return Task.cont

  def parseinput(self, input):
    ''' parse the messages received by the server and make them human readable
    '''
    color = self.defaultColor
    if self.svrmsg.match(input) is not None:
      #print "svrmsg '%s'" % input
      # Server message
      parse = self.svrmsg.match(input)
      result = "svr: %s: %s" % (parse.group(1), parse.group(2))
      color = self.svrmsgColor
    elif self.chanmsg.match(input) is not None:
      #print "chanmsg '%s'" % input
      # Channel msg
      color = self.chanmsgColor
      parse = self.chanmsg.match(input)
      if parse.group(4).upper() == "PRIVMSG":
        result = "chan: [#%s : %s]: %s" % (parse.group(5), parse.group(1), parse.group(6))
      else:
        # Unhandled
        result = input.rstrip()
    elif self.genmsg.match(input) is not None:
      #print "genmsg '%s'" % input
      # General messages
      parse = self.genmsg.match(input)
      if parse.group(4).upper() == "QUIT":
        result = "gen: -- %s has quit: %s" % (parse.group(1), parse.group(5))
      elif parse.group(4).upper() == "JOIN":
        result = "gen: ++ %s has joined: %s" % (parse.group(1), parse.group(5))
      elif parse.group(4).upper() == "NICK":
        result = "gen: -+ %s has renamed into %s" % (parse.group(1), parse.group(5))
      else:
        # Unhandled input
        result = input.rstrip()
      color = self.genmsgColor
    elif self.pingmsg.match(input):
      parse = self.pingmsg.match(input)
      raise PingInputError, parse.group(1)
    elif self.pongmsg.match(input):
      result = ''
    else:
      color = self.unhandledmsgColor
      if len(input) > 0:
        result = "unh: %s" % input.rstrip()
      else:
        result = ""
    return result, color

  def parsecmd(self, input):
    '''parse the user supplied input and reformat into IRC commands
    '''
    # If first char is a /, then this is a command.
    output = input
    color = self.defaultColor
    if input[0] == "/" :
      try:
        parsedcmd = self.usercmd.match(input)
        command = parsedcmd.group(1).upper() # group(0) is the raw match, not the group
        if (command == "MSG") :
          color = self.messageColor
          # private message to a user.  format: /msg user text
          # break off the first word of group(3) to get userid
          splitcmd = self.usermsg.match(parsedcmd.group(3))
          output = "PRIVMSG %s : %s" % (splitcmd.group(1), splitcmd.group(3))
        elif (command == "JOIN"):
          color = self.joinmsgColor
          # Only supports one channel, no keys, at this time
          if parsedcmd.group(3) is not None:
            output = "%s %s" % (command, parsedcmd.group(3))
            # Store channel for later use
            self.channel = parsedcmd.group(3)
          else :
            # Raise a USER=ID10T error
            pass
        elif (command == "CONNECT"):
          color = self.connectmsgColor
          if parsedcmd.group(2) is not None:
            self.connect( parsedcmd.group(2).strip() )
        elif (command == "QUIT"):
          color = self.disconnectColor
          # map add'l params i.e. reason for quitting
          if parsedcmd.group(3) is not None:
            output = "%s :%s" % (command, parsedcmd.group(3))
          self.disconnect()
        elif (command == "PART"):
          color = self.partmsgColor
          # add'l param = channel to leave
          if parsedcmd.group(3) is not None:
            output = "%s %s" % (command, parsedcmd.group(3))
        elif (command == "NICK"):
          color = self.nickmsgColor
          output = "NICK %s" % parsedcmd.group(3)
      except Exception, inst:
        self.outputCallBack( "Unexpected error in ircClientClass:\n- %s\n- %s\n- %s\n- %s" % \
                            ( str(sys.exc_info()[0])
                            , str(sys.exc_info()[1])
                            , '\n'.join(traceback.format_tb(sys.exc_info()[2], 10))
                            , "'%s'" % input), '# ', self.exceptionColor )
        output = ''
    elif input[0] == "#" :
      color = self.prvmsgColor
      splitcmd = self.usermsg.match(input)
      output = "PRIVMSG %s :%s" % (splitcmd.group(1), splitcmd.group(3))
    else:
      color = self.prvmsgColor
      # send the message to the stored channel
      output = "PRIVMSG %s :%s" % (self.channel, output)
    return output.rstrip(), color
  
  def autocomplete( self, ircText, currentPosition ):
    
    newText = ircText
    printText = None
    
    if len(ircText) > 0:
      # if its the first word
      if len(ircText.split(' ')) == 1:
        # if its a irc command
        if ircText[0] == '/':
          ircText = ircText[1:].upper()
          out = completeIrcCommand( ircText )
          if len(out) == 1:
            newText = "/%s " % out[0]
          else:
            printText =  ' '.join(out)
    return newText, printText
  
  def autohelp( self, ircText, currentPosition ):
    printText = ''
    return printText