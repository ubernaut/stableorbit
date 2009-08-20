import re

# dont know why this doesnt work correctly
builtinsEnviron = dir(__builtins__)
# this does for sure
builtinsEnviron = [ 'ArithmeticError', 'AssertionError', 'AttributeError'
  , 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EnvironmentError'
  , 'Exception', 'False', 'FloatingPointError', 'FutureWarning'
  , 'IOError', 'ImportError', 'IndentationError', 'IndexError'
  , 'KeyError', 'KeyboardInterrupt', 'LookupError'
  , 'MemoryError', 'NameError', 'None', 'NotImplemented'
  , 'NotImplementedError', 'OSError', 'OverflowError', 'OverflowWarning'
  , 'PendingDeprecationWarning', 'ReferenceError', 'RuntimeError'
  , 'RuntimeWarning', 'StandardError', 'StopIteration', 'SyntaxError'
  , 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'True'
  , 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError'
  , 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError'
  , 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError'
  , '__debug__', '__doc__', '__import__', '__name__', 'abs', 'apply'
  , 'basestring', 'bool', 'buffer', 'callable', 'chr', 'classmethod'
  , 'cmp', 'coerce', 'compile', 'complex', 'copyright', 'credits'
  , 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'execfile'
  , 'exit', 'file', 'filter', 'float', 'frozenset', 'getattr', 'globals'
  , 'hasattr', 'hash', 'help', 'hex', 'id', 'in ', 'input', 'int', 'intern'
  , 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals'
  , 'long', 'map', 'max', 'min', 'object', 'oct', 'open', 'ord', 'pow', 'print '
  , 'property', 'quit', 'range', 'raw_input', 'reduce', 'reload', 'repr'
  , 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod'
  , 'str', 'sum', 'super', 'tuple', 'type', 'unichr', 'unicode', 'vars'
  , 'xrange( ', 'zip', 'for ']

'''ircEnviron = [ 'ADDBUTTON', 'ALLCHAN', 'ALLCHANL', 'ALLSERV', 'AWAY', 'BACK'
  , 'BAN', 'CHANOPT', 'CHARSET', 'CLEAR', 'CLOSE', 'COUNTRY', 'CTCP', 'CYCLE'
  , 'DCC', 'DEBUG', 'DEHOP', 'DELBUTTON', 'DEOP', 'DEVOICE', 'DISCON', 'DNS'
  , 'ECHO', 'EXEC', 'EXECCONT', 'EXECKILL', 'EXECSTOP', 'EXECWRITE', 'FLUSHQ'
  , 'GATE', 'GETFILE', 'GETINT', 'GETSTR', 'GHOST', 'GUI', 'HELP', 'HOP', 'ID'
  , 'IGNORE', 'INVITE', 'JOIN', 'KICK', 'KICKBAN', 'KILLALL', 'LAGCHECK'
  , 'LASTLOG', 'LIST', 'LOAD', 'MDEHOP', 'MDEOP', 'ME', 'MENU', 'MKICK', 'MODE'
  , 'MOP', 'MSG', 'NAMES', 'NCTCP', 'NEWSERVER', 'NICK', 'NOTICE', 'NOTIFY'
  , 'OP', 'PART', 'PING', 'QUERY', 'QUIT', 'QUOTE', 'RECONNECT', 'RECV', 'SAY'
  , 'SEND', 'SERVCHAN', 'SERVER', 'SET', 'SETCURSOR', 'SETTAB', 'SETTEXT'
  , 'SPLAY', 'TOPIC', 'TRAY', 'UNBAN', 'UNIGNORE', 'UNLOAD', 'URL', 'USELECT'
  , 'USERLIST', 'VOICE', 'WALLCHAN', 'WALLCHOP' ]'''

ircEnviron = [ 'CONNECT', 'QUIT', 'NICK', 'PRIVMSG', 'JOIN', 'PART', 'LIST' ]

#class autocompleterClass:
#  def __init__( self ):
#    pass
  
def help( self ):
  return """ ------ autocompletion ------
TAB    : autocomplete
BUGS   : currently only available in panda3d window"""

def completeIrcCommand( ircText ):
  lastWordSplit = ircText.split(' ')
  environs = { '': ircEnviron }
  search = re.compile( '^%s.*$' % lastWordSplit[-1] )
  
  matchList = list()
  for envPre, envObjList in environs.items():
    for envObj in envObjList:
      if re.match( search, envObj ):
        if envPre:
          envFound = "%s.%s" % (envPre, envObj)
        else:
          envFound = envObj
        matchList.append( envFound )
  return matchList
  
def completePython( parent, pythonText ):
  matchList = []
  
  pythonTestSplit = pythonText.strip().split(' ')
  lastWord = pythonTestSplit[-1]
  
  lastWordSplit = lastWord.split('.')
  currentEnviron = '.'.join(lastWordSplit[:-1])
  
  if currentEnviron == '':
    allEnv = builtinsEnviron[:]
    allEnv.extend( parent.keys() )
    environs = { '': allEnv }
  else:
    environs = { currentEnviron: dir(parent[lastWordSplit[0]]) }
    if len(lastWordSplit) > 2:
      execCmd = "cv = dir( parent[lastWordSplit[0]].%s )" % (".".join(lastWordSplit[1:-1]))
      exec( execCmd )
      environs = { currentEnviron: cv }
  
  search = re.compile( '^%s.*$' % lastWordSplit[-1] )
  
  matchList = list()
  for envPre, envObjList in environs.items():
    for envObj in envObjList:
      if re.match( search, envObj ):
        if envPre:
          envFound = "%s.%s" % (envPre, envObj)
        else:
          envFound = envObj
        matchList.append( envFound )
  
  return matchList
