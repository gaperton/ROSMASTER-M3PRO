# config.txt file description

Check status file format Common options GPIO control

illustrate

config.txt is a startup configuration file unique to the Raspberry Pi system. It is located on the first (boot) partition of the SD card and is read by the GPU before initializing the ARM CPU and Linux.

```
Raspberry Pi OS config.txt path: /boot/config.txt
```

## Check status

Use the following command to view the current option settings:

Display specific configuration values: vcgencmd get_config

```
Example: vcgencmd get_config arm_freq
```

List all integer configuration options that have been set (non-zero)

```
vcgencmd get_config int
```

List all string configuration options that have been set (non-zero)

```
vcgencmd get_config str
```

## file format

file format:

- 1. A single statement per line, the content is an integer or a string
- 2. Comment: Add # at the beginning of the line

A line of comments can be added before each statement to explain the function of the statement. The length of each line is limited to 98 characters. Content exceeding the limit will be ignored.

```
#Example:
# Enable audio (loads snd_bcm2835)
dtparam=audio=on
# Automatically load overlays for detected cameras
camera_auto_detect=1
# Automatically load overlays for detected DSI displays
display_auto_detect=1
# Enable DRM VC4 V3D driver
dtoverlay=vc4-kms-v3d
```

# Common options

## camera_auto_detect

When this setting is enabled, the firmware will automatically load overlays for the CSI cameras it recognizes.

Set to disabled:

```
camera_auto_detect=0
```

### display_auto_detect

When this setting is enabled, the firmware will automatically load overlays for the DSI monitors it recognizes.

Set to disabled:

```
display_auto_detect=0
```

#### dtoverlay

Used to load and configure device tree overlays. By configuring dtoverlay, users can add additional hardware support or functionality to the Raspberry Pi system.

Load an overlay that enables the kernel graphics driver:

```
dtoverlaydtoverlay=vc4-kms-v3d
```

## GPIO control

Set GPIO pins to specific modes and values at startup without using custom files.

Set the same pattern of pins per line: can be a single pin, a range of pins, or a comma-separated list of pins;

The pin settings are followed by one or more comma-separated properties.

| Abbreviation | Full name                  | Meaning                          |
|--------------|----------------------------|----------------------------------|
| IP           | Input                      | input                            |
| op           | Output                     | output                           |
| a0-a5        | Alt0-Alt5                  | Multiplexing                     |
| dh           | Driving high (for outputs) | High level driving (for outputs) |
| dl           | Driving low (for outputs)  | Low level driving (for outputs)  |
| pu           | Pull up                    | pull up                          |
| pd           | Pull down                  | pull down                        |
| pn/np        | No pull                    | No pull-down                     |

### Example:

```
# Select Alt2 for GPIO pins 0 to 27 (for DPI24)
gpio=0-27=a2
# Set GPIO12 to be an output set to 1
gpio=12=op,dh
# Change the pull on (input) pins 18 and 20
gpio=18,20=pu
# Make pins 17 to 21 inputs
gpio=17-21=ip
```

## illustrate

Only some of the options are listed here. For more detailed information, please go to the official website!

https://www.raspberrypi.com/documentation/
