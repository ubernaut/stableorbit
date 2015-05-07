# User Manual #

This wiki page describes how to configure run and navigate solarClient.py

# Launching the Client #

Once Python and Panda3D are installed, and stableorbit is extracted to a location of your choosing. Open the folder containing stableorbit either through a file-browser or command-line. once there You can launch the client by double-clicking 'solarClient.bat' in Windows or typing 'python solarClient.py' from the command line.

A black window should launch. It will remain black for a few seconds while the client attepts to connect to the server and either retrieves a series of systems from the server or generates it's own if a connection problem is encountered. During this period the text in the console describes the status of the client and will look something like this:

cos@chunk:~/stableorbit$ python solarClient.py
DirectStart: Starting the game.
Known pipe types:
> glxGraphicsPipe
(all display modules loaded.)
connecting to server http://bamdastard.kicks-ass.net:8000
connection acquired
retrieving a system
converting xfile
launching evaluator
calculating score
system stability score =
2.62619423771
retrieving a system
converting xfile
launching evaluator
calculating score
system stability score =
5.85486589733

This will continue until a system with a stability below 1.0  is found. The text in the console will state 'found acceptable system, recording system as: '. The next line reveals the  system name recorded by the server, this can be used to retrieve and view the system later. An example of the console output is shown below:

system stability score =
0.999404387469
found acceptable system, recording system as:
system15.sys
launching planetarium.. .  .    .        .

Afterwards the stars will load into the black window and you'll know the client has received or generated an acceptable system.

The system is now loaded but we are too close to see it. Hold the right-mouse button and push your mouse slowly up to zoom out.

# Client Navigation #
> The mouse is used to change views while using the client.

  * The left-mouse button is used for panning
  * The middle mouse button is used for rotation
  * The right mouse button is used to zooming in and out.


# Client Configuration #

The Client was designed to be a passive screensaver.  With this in mind I decided alternate functionality should be achived by launching the solarClient class with different arguments. To change these runtime arguments open solarClient.py in a text editor and scroll to the bottom.

#Uncomment the following line to retrieve "system6" from the server
#defaultClient = solarClient('http://bamdastard.kicks-ass.net:8000', 1, "system10.sys")

#Uncomment the following line if you want the client to run offline
#defaultClient = solarClient("standalone",1, "none")

#this is the default configuration which attempts to retrieve a system from
#the server. Failure will cause the client to launch locally in disconnected mode
defaultClient = solarClient()

The first comment block above is an example which retrieves "system10.sys" from the server and launches it using the planetarium. Example client console output is pictured below:

connecting to server
http://bamdastard.kicks-ass.net:8000
attempting to retrieve and launch system:
system10.sys
unpacking system
launching evaluator
calculating score
system stability score =
0.997394952702
launching planetarium.. .  .    .        .

The Second comment block shows how to launch the client in disconnected mode.

# Server Configuration #

If you wish to run your own SolarServer.py you can do so by simply changing the IP address located at the bottom of 'solarServer.py' to reflect your IP address. The client then must also be launched with the same IP address as an argument.