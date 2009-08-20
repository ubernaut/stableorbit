# --- define your settings here ---

# output debug informations
DEBUG = True

# command which causes the help to be shown
HELP_COMMAND       = 'help'
# all of the following must be eighter a single character or None
# None means its allways (except on exclude) active
# call the python interpreter in this character
PYTHON_PRE         = None
# dont call the python interpreter on this character
PYTHON_PRE_EXCLUDE = '!'
# call the irc on this character
IRC_PRE            = '!'
# dont call it on this character
IRC_PRE_EXPLUCE    = None

# after what time should keys be read from the command line
# if set to None, taskMgr.add will be used instead of taskMgr.doMethodLater
TERMINAL_TASK_TIME = None

# after what time should the network port be polled
# if set to None, taskMgr.add will be used instead of taskMgr.doMethodLater
# setting this value to large might drop data received from the server
IRC_TASK_TIME = 0.05


AUTOCOMPLETER = True
AUTOCOMPLETER_INFOTEXT_COLOR = (0.8,0.8,0.8,1.0)

HELP_INFOTEXT_COLOR = (0.8,1.0,0.8,1.0)


# --- variables for the panda3d console ----
# default color of the panda3d font
DEFAULT_COLOR = (1,1,1,1)
# toggle key to show/hide the panda3d console
PANDA3D_CONSOLE_TOGGLE_KEY = "f10"
PANDA3D_CONSOLE_AUTOCOMPLETE_KEY = "tab"
PANDA3d_CONSOLE_AUTOHELP_KEY = "f1"
# font to be used
PANDA3D_CONSOLE_FONT = 'data/interactiveConsole/vera.ttf'
# this value has to be determined manually,
# it is used to calculate number of characters on a line
PANDA3D_CONSOLE_FONT_WIDTH = 0.5
# the size & position of the panda3d window
PANDA3D_CONSOLE_SCALE = 0.04
PANDA3D_CONSOLE_HORIZONTAL_POS = 0.35
PANDA3D_CONSOLE_HORIZONTAL_SIZE = 1.9
PANDA3D_CONSOLE_VERTICAL_POS = 0.05
PANDA3D_CONSOLE_VERTICAL_SIZE = 1.9
# to change the alignment of the console
# look into the panda3d.py def windowEvent


# --- things after this line should not be changed ---

# some constants
INPUT_GUI = 1
INPUT_CONSOLE = 2
OUTPUT_PYTHON = 3
OUTPUT_IRC = 4

