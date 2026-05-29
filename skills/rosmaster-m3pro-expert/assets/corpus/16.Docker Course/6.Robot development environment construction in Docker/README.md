# 6. Robot development environment construction in Docker

#### 6. Robot development environment construction in Docker

```
6.1、Using Jupyter Lab to access Docker
```

6.2、Use vscode to access docker

6.2.1、Remote configuration

6.2.2、vscode configuration

6.2.2.1、download and install VSCODE

6.2.2.2、vscode configuration ssh remote login to the host

6.2.2.3、enter the robot container

6.2.2.4、Vscode remote host configuration docker environment

6.2.2.5、Configure passwordless login

The operating environment and software and hardware reference configurations are as follows:

- Reference model: ROSMASTER X3
- Robot hardware configuration: Arm series main control, Silan A1 lidar, AstraPro Plus depth camera
- Robot system: Ubuntu (version not required) + docker (version 20.10.21 and above)
- PC Virtual Machine: Ubuntu (20.04) + ROS2 (Foxy)
- Usage scenario: Use on a relatively clean 2D plane

## 6.1. Using Jupyter Lab to access Docker

1. Enter the container, see [5. Enter the docker container of the robot], and execute the following command:

Note: When using Jupyter Lab in a docker container, you must run the docker container as host: add the "--net=host" parameter when running the container

```
root@ubuntu:/# jupyter lab --allow-root
[I 2023-04-24 09:27:45.265 ServerApp] Package jupyterlab took 0.0001s to import
[I 2023-04-24 09:27:45.277 ServerApp] Package jupyter_server_fileid took 0.0096s to
import
[I 2023-04-24 09:27:45.297 ServerApp] Package jupyter_server_terminals took 0.0190s
to import
[I 2023-04-24 09:27:45.429 ServerApp] Package jupyter_server_ydoc took 0.1301s to
import
[I 2023-04-24 09:27:45.431 ServerApp] Package nbclassic took 0.0001s to import
..................
```

2. Other devices view, open in Windows or Ubuntu browser (must be under the same LAN, 192.168.2.102 is the IP address in the docker container)

http://192.168.2.102:8888/lab

Enter the password: Yahboom enter Jupyter Lab

![Picture: page 1: picture 2](_page_1_Picture_2.jpeg)

The following directory is the project path of the bot:

![Picture: page 1: picture 4](_page_1_Picture_4.jpeg)

## 6.2. Use vscode to access docker

Let's take the example of configuring VSCODE to access the Docker container in Windows, and the steps to access Docker in Ubuntu are basically the same.

### 6.2.1. Remote configuration

See [VI. Linux Operating System---- 3. Remote Control] chapter

Make sure Windows can telnet to the Docker host [car]:

```
Open cmd in windows enter ssh command test: ssh jetson@192.168.2.102 (username and
ip modified to own)
Or use remote tools: putty, xshell, securecrt, winscp, mobaxterm, finalshell, etc
```

### 6.2.2. vscode configuration

#### 6.2.2.1. download and install VSCODE

VSCODE official website:<https://code.visualstudio.com/>, download the installation of the Windows version

#### 6.2.2.2. vscode configuration ssh remote login to the host

1. Open vscode, click the icon of the arrow at the bottom left, then enter remote in the search box, select the Remote Development plugin, and click Install to install the plugin

![Picture: page 2: picture 9](_page_2_Picture_9.jpeg)

vscode is installed by default and then in English, and you can install Chinese plugins to localize:

![Picture: page 2: picture 11](_page_2_Picture_11.jpeg)

2. Press the shortcut key [Ctrl + Shift + P] in VSCODE to open the command input window, type: remote, and then log in to the remote host [car] according to the instructions shown below.

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)

![Picture: page 4: picture 0](_page_4_Picture_0.jpeg)

How to see the screen shown above, indicating that you have successfully logged in to the host computer.

#### 6.2.2.3. enter the robot container

See the tutorial in the [5. Enter the docker container of the robot] chapter.

#### 6.2.2.4. Vscode remote host configuration docker environment

1. Install the docker plug-in on the remote host [car].

![Figure: page 5: figure 1](_page_5_Figure_1.jpeg)

2. After the installation is completed, a docker icon will appear in the left navigation bar

![Figure: page 6: figure 0](_page_6_Figure_0.jpeg)

3. Click the docker icon

![Figure: page 7: figure 0](_page_7_Figure_0.jpeg)

4. Right-click the running container and operate as shown below:

![Figure: page 8: figure 0](_page_8_Figure_0.jpeg)

5. A new window will open and see the following indicates that it has entered the container

![Picture: page 8: picture 3](_page_8_Picture_3.jpeg)

6. Open the folder

/root/yahboomcar_ros2_ws # This is the project path for the bot

# Visual Studio Code

## 编辑进化

## 启动

1 新建文件...

打开文件...

打开文件夹...

克隆 Git 仓库...

### 最近

nx-Wi-Fi] /root/yahboomcar_ros2_ws [Container yahboomtechnology/ros-foxy:3....
yahboomcar_ros2_ws C:\Users\Admin\Desktop\nx-ros2
jetson nano_x1的出厂镜像代码 C:\Users\Admin\Desktop
originbot C:\Users\Admin\Desktop\workspace
nx-Wi-Fi] ~/yahboomcar_ros2_ws [Container yahboomtechnology/ros-foxy:3.3.7 (...
更多...

![Figure: page 9: figure 9](_page_9_Figure_9.jpeg)

![Figure: page 10: figure 0](_page_10_Figure_0.jpeg)

![Figure: page 11: figure 0](_page_11_Figure_0.jpeg)

7. Similarly, we can also install the plug-ins we need in the container to facilitate our development

![Figure: page 12: figure 0](_page_12_Figure_0.jpeg)

In addition to ROS, the recommended plugins to install here are:

![Figure: page 13: figure 0](_page_13_Figure_0.jpeg)

After completing the above steps, you can manipulate the code files in the container to develop and learn.

#### 6.2.2.5. Configure passwordless login

In the above steps, some steps may require entering the password of the host, here is another optimization, configure passwordless login.

1. First test using SSH to log in to the host [car] in Windows, the instructions are as follows:

```
ssh jetson@192.168.2.102 (username and IP modified to own)
```

At this time, you will find that you need to enter the host password

- 2. Next, configure password-free login
- (1) Add environment variables

Open the environment variable properties page, click New in the user variables section, the variable is HOME, the value is C:Usersname, where name is the user name, you can view the user name of your own computer, and then the generated key pair is saved in this directory by default.

![Figure: page 14: figure 3](_page_14_Figure_3.jpeg)

#### (2) Generate a key pair

Open the cmd command line, run it in the directory where the ssh program is located, or run [sshkeygen -t rsa] anywhere after adding the system environment to generate the key, and then enter all the way, when you see a histogram generated, then the key is generated successfully. At this time, there will be two more files under the.ssh folder of the user directory, namely id_rsa (private key) and id_rsa.pub (public key)

![Figure: page 15: figure 0](_page_15_Figure_0.jpeg)

(3) Add the public key to the host

Similarly, open the cmd command line, enter

```
ssh username@host "cat >> ~/.ssh/authorized_keys" < C:Usersname.sshid_rsa.pub
#For example: Modify ssh jetson@192.168.2.102 "cat >> ~/.ssh/authorized_keys" <
C:UsersAdmin.sshid_rsa.pub
```

This command first logs in to the host, and then adds the public key under the local computer, i.e. win, to the personal directory of the host account to achieve password-free login. Note that this step requires the password of the host account.

(4) Verification

Test again using ssh in Windows to log in to the host [trolley], the command is as follows:

```
ssh jetson@192.168.2.102 (username and IP modified to own)
```

At this time, you will find that you no longer need to enter the password.

Restart VSCODE, and where you need to enter a password, you don't need to enter a password.
