# **Using MIPI camera**

#### **Using MIPI [camera](#page-0-0)**

<span id="page-0-0"></span>[Configure](#page-0-1) camera Use [camera](#page-1-0) [Preview](#page-1-1) camera [Photograph](#page-1-2) [rpicam-still](#page-1-3) [Video](#page-2-0) [rpicam-vid](#page-2-1) Error [resolution](#page-2-2) [Web page](#page-4-0) preview camera Run [script](#page-4-1) [Web access](#page-5-0)

The Raspberry Pi 5 combines the previous CSI and DSI interfaces into two dual-purpose CSI/DSI (MIPI) ports.

# <span id="page-0-1"></span>**Configure camera**

When using a Raspberry Pi camera or a third-party camera, you can modify the camera configuration according to the following table:

| Camera module               | File located at: /boot/firmware/config.txt                                                                                                                                                                        |
|-----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| V1 Camera (OV5647)          | dtoverlay=ov5647                                                                                                                                                                                                  |
| V2 camera (IMX219)          | dtoverlay=imx219                                                                                                                                                                                                  |
| HQ Camera (IMX477)          | dtoverlay=imx477                                                                                                                                                                                                  |
| GS camera (IMX296)          | dtoverlay=imx296                                                                                                                                                                                                  |
| Camera module 3<br>(IMX708) | dtoverlay=imx708                                                                                                                                                                                                  |
| IMX290 and IMX327           | dtoverlay=imx290,clock-frequency=74250000<br>or (both modules share the IMX290 kernel driver; for the correct<br>frequency,<br>see the module vendor's instructions)<br>dtoverlay=imx290,clock-frequency=37125000 |
| IMX378 type                 | dtoverlay=imx378                                                                                                                                                                                                  |
| OV9281 series               | dtoverlay=ov9281                                                                                                                                                                                                  |

If you are not using the official Raspberry Pi camera, you can modify the config.txt file as shown in the table and add the dtoverlay content to the /boot/firmware/config.txt file.

sudo nano /boot/firmware/config.txt

For example: Raspberry Pi uses IMX219 camera, connect the camera to the Raspberry Pi J4 interface, and then modify the /boot/firmware/config.txt file:

![](_page_1_Picture_1.jpeg)

To use the IMX219 camera, it needs to be connected to the J4 interface of Raspberry Pi 5 for recognition!

Modify the configuration file and restart to take effect!

## **Use camera**

# **Preview camera**

<span id="page-1-1"></span><span id="page-1-0"></span>rpicam-hello

Entering this command in the terminal will display the preview window for about 5 seconds.

rpicam-hello -t 0

Running this command in the terminal will always display the preview window. You can use the window close button and Ctrl+C to exit!

# **Photograph**

<span id="page-1-2"></span>rpicam-jpeg -o test.jpg

Display a preview for 5 seconds, then capture the image and save it as a test.jpg file

<span id="page-1-3"></span>rpicam-jpeg -o test.jpg -t 2000 --width 640 --height 480

Show a preview for 2 seconds, then capture and save the image as a test.jpg file, with the image having a width of 640 pixels and a height of 480 pixels.

### **rpicam-still**

This command can be used to save files in different formats:

```
rpicam-still -e png -o test.png
rpicam-still -e bmp -o test.bmp
rpicam-still -e rgb -o test.data
rpicam-still -e yuv420 -o test.data
```

Raw image capture

```
rpicam-still -r -o test.jpg
```

Time-lapse shooting

Capture images continuously at intervals of 2 seconds for a total capture duration of 30 seconds, and save each image as a file name similar to image0001.jpg:

```
rpicam-still -t 30000 --timelapse 2000 -o image%04d.jpg
```

# **Video**

### <span id="page-2-1"></span>**rpicam-vid**

Commands for video recording using the camera module on the Raspberry Pi.

Example: Record 10 seconds of video and write to test.h264 file

```
rpicam-vid -t 10000 -o test.h264
```

play video

```
vlc test.h264
```

**Note**: If the test.h264 file cannot be played and an error occurs, please try the following method to solve it.

#### <span id="page-2-2"></span>**Error resolution**

Modify the frame rate of H264 playback per second

![](_page_3_Figure_0.jpeg)

![](_page_3_Figure_1.jpeg)

![](_page_4_Figure_0.jpeg)

# <span id="page-4-0"></span>**Web page preview camera**

Use Python script files to preview camera images on web pages.

### <span id="page-4-1"></span>**Run script**

Code path:/home/pi/Camera\_Web\_Preview/

cd /home/pi/Camera\_Web\_Preview/ python3 mjpeg\_server.py

### <span id="page-5-0"></span>**Web access**

Devices under the same LAN can enter :8000 through the browser to view the real-time camera view!

Example: Raspberry Pi IP: 10.42.0.1 Web access: 10.42.0.1:8000

![](_page_6_Figure_0.jpeg)

# **Picamera2 MJPEG Streaming Demo**

![](_page_6_Picture_2.jpeg)

If you want to set up auto-start at boot, you can search for information online and set the script file to auto-start at boot!