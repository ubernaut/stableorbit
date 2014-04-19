OculusOverlay dev preview 0.7 - http://holophone3d.com/oculus

Thanks for trying out the OculusOverlay the easy way to instantly view any 2D or 3D content from any application in your OculusRift.  
The OculusOverlay works by capturing the specified desktop region in near real time and warping it into a Rift view.
For example, on my 4+ year old Corei7 with a GeForce 550 I'm seeing 60+ fps capturing regions of 1280x800.
This app DISABLES Aero glass to substantially improve capture performance (only for Win7/Vista), it will re-enable it on exit. Also, you can control it in the app below.

Usage:
  NOTE: This app requires the XNA 4.0 redist, get it here: http://www.microsoft.com/en-us/download/details.aspx?id=20914
  All content must be in a Windowed mode to be captured (i.e. full screen games won't be captured)
  You must set screen region and choose viewing mode - see instructions below
  Default Overlay window is 1280 x 800, use extended desktop and use the 'Z' command to push to Rift screen
  REMEMBER: The overlay window must have focus to recieve the commands below -if commands aren't working, click back on the overlay window to set focus

New App Conifg Support (Open OculusOverlay.config to set defaults)
<?xml version="1.0" encoding="utf-8" ?>
<configuration>
  <appSettings>
    <add key="ViewMode" value="Split"/>             <!--Values=Split,Duplicate--> 
    <add key="CaptureRegion" value="0,0,1280,800"/> <!--Values=x1,y1,x2,y2 where x1&y1 are topLeft and x2&y2 are width and height -->
    <add key="CaptureMode" value="Sync"/>           <!--Values=Sync,Async-->
    <add key="ShowMouseCursor" value="False"/>      <!--Values=True,False-->
  </appSettings>
</configuration>

Commands

Save new defaults
  Save current settings as defaults = S

Set Capture Region
  Set Top Left Corner = Hold Y and move mouse to top left corner of desired capture region 
  Set Bottom Right Corner = Hold H and move mouse to bottom right corner of desired capture region

Viewing Modes
  SplitMode (default) - used for SideBySide 3D content, keep pressing to toggle 'full Width' vs. 'Half width' mode = A
  DuplicateMode - used for viewing 2D content = Q

Set Capture sync mode
  Synchronous - slightly slower, more stable  = R	
  Async (default) - ~20% smoother slightly higher  latency, not as stable = F

Zoom
  Zoom In = J
  Zoom Out = U

Horizontal/Paralax adjustment
  Move In = K
  Move Out = I

FullScreen modes (under development)
  Auto set to fullScreen on Rift = Z
  Restore Window to previous position = X

Mouse Cursor
 Show mouse = E (sets the cursor to the currently displayed cursor)
 Hide mouse = D

Distortion Scale
 Increase distortion = P (Max is Rift default distortion)
 Decrease distortion = O (Min is -.14 which lets you add inverse distortion, just in case that is cool)

Enable/Disable DWM (Desktop Window Manager/Aero Glass)
 Enable DWM = N (Application will always re-enable DWM on exit)
 Disable DWM = M