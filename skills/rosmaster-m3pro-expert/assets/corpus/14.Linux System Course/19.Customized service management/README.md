# 19.Customized service management

## 1. Create a new service file

Create a new yahboom_oled.service in the user directory

```bash
touch yahboom_oled.service
vim yahboom_oled.service
```

Add the following content, where User represents the user name and needs to be modified according to the actual user name;

ExecStart represents the command to be executed and the command needs to be executed according to the actual modification.

Jetson Nano system service files:

```
[Unit]
Description=yahboom_oled start service
After=multi-user.target
[Service]
Type=idle
User=jetson
ExecStart=/bin/sh -c "python3
/home/jetson/software/oled_yahboom/yahboom_oled.py"
WorkingDirectory=/home/jetson
[Install]
WantedBy=multi-user.target
```

Raspberry Pi system service file:

```
[Unit]
Description=yahboom_oled start service
After=multi-user.target
[Service]
Type=idle
User=pi
ExecStart=/bin/sh -c "python3 /home/pi/software/oled_yahboom/yahboom_oled.py"
WorkingDirectory=/home/pi
[Install]
WantedBy=multi-user.target
```

Then exit editing and enter: qw to save the file.

## 2. Update service

Copy the newly created yahboom_oled.service service file to the /etc/systemd/system/ path.

```bash
sudo cp yahboom_oled.service /etc/systemd/system/
```

Update system services

```bash
sudo systemctl daemon-reload
```

## 3. Management services

Check service status

```bash
sudo systemctl status yahboom_oled.service
```

Start service

```bash
sudo systemctl start yahboom_oled.service
```

Restart service

```bash
sudo systemctl restart yahboom_oled.service
```

Set the service to automatically start at boot

```bash
sudo systemctl enable yahboom_oled.service
```

Close service

```bash
sudo systemctl stop yahboom_oled.service
```

Service does not start when booting

```bash
sudo systemctl disable yahboom_oled.service
```
