     _______.___________.    ___      .______    __       _______   ______   .______      .______    __  .___________.
    /       |           |   /   \     |   _  \  |  |     |   ____| /  __  \  |   _  \     |   _  \  |  | |           |
   |   (----`---|  |----`  /  ^  \    |  |_)  | |  |     |  |__   |  |  |  | |  |_)  |    |  |_)  | |  | `---|  |----`
    \   \       |  |      /  /_\  \   |   _  <  |  |     |   __|  |  |  |  | |      /     |   _  <  |  |     |  |     
.----)   |      |  |     /  _____  \  |  |_)  | |  `----.|  |____ |  `--'  | |  |\  \----.|  |_)  | |  |     |  |     
|_______/       |__|    /__/     \__\ |______/  |_______||_______| \______/  | _| `._____||______/  |__|     |__|     
                                                                                                                     
http://code.google.com/p/stableorbit
StableOrbit
----------------------------------------------------
Installation:
----------------------------------------------------
In order to run this you'll need Panda3d you can fetch that from here:

http://www.panda3d.org/download.php?sdk&version=1.8.1

After that you can simply run soSession.py  or if you're using windows you'll need to use the batch script. 

Windows:
run StableOrbit.bat 

MacOS/Linux

python soSession.py


----------------------------------------------------
Configuration:
----------------------------------------------------
In soSession.py you can change the following variables on line 27 to your needs. 
   
   def __init__(self, args=["fullscreen 0","win-size 1440 900","side-by-side-stereo 0", "undecorated 1"]):
   
"fullscreen 1" for fullscreen
"win-size 1920 1080" for a 1080p resolution (or any other resolution you want
"undecorated 0" to enable window borders

----------------------------------------------------
Oculus Rift support:
----------------------------------------------------
Configure your rift to display as a separate 'extended desktop' and do not set it as the primary display. 

Launch the included oculus overlay executable 

in soSession.py

Set 
"win-size 1280 800"
"side-by-side-stereo 1"
"fullscreen 0"

or args=["fullscreen 0","win-size 1280 720","side-by-side-stereo 1", "undecorated 0"]):


run stableorbit with either python soSession.py or the stableOrbit.bat (if using windows). 

move the stableorbit window to the far top left of your primary display and you're in business!

controls:
escape= exit

space=stop
d=brake
e=accelerate

wheel_right= tiltLeft
wheel_left= tiltRight
wheel_up= zoomIn
wheel_down= zoomOut

m=togglemap
[=scaleDown acceleration
]=scaleUp acceleration
l or middle mouse=togglemouselook


 