# 6、Robot development environment
# construction in Docker
## 6、Robot development environment construction in Docker
### 6.1、Using Jupyter Lab to access Docker

### 6.2、Use vscode to access docker

#### 6.2.1、Remote configuration

#### 6.2.2、vscode configuration

##### 6.2.2.1、download and install VSCODE

##### 6.2.2.2、vscode configuration ssh remote login to the host

##### 6.2.2.3、enter the robot container

##### 6.2.2.4、Vscode remote host configuration docker environment

##### 6.2.2.5、Configure passwordless login


The operating environment and software and hardware reference configurations are as follows:


Reference model: ROSMASTER X3


Robot hardware configuration: Arm series main control, Silan A1 lidar, AstraPro Plus depth

camera


Robot system: Ubuntu (version not required) + docker (version 20.10.21 and above)


PC Virtual Machine: Ubuntu (20.04) + ROS2 (Foxy)


Usage scenario: Use on a relatively clean 2D plane
### 6.1、Using Jupyter Lab to access Docker
1. Enter the container, see [5. Enter the docker container of the robot], and execute the following

command:


Note: When using Jupyter Lab in a docker container, you must run the docker container as host: add

the "--net=host" parameter when running the container


2. Other devices view, open in Windows or Ubuntu browser (must be under the same LAN,

192.168.2.102 is the IP address in the docker container)


![](6、Robot-development-environment-construction-in-Docker.pdf-0-0.jpeg)
The following directory is the project path of the bot:

### 6.2、Use vscode to access docker
Let's take the example of configuring VSCODE to access the Docker container in Windows, and the

steps to access Docker in Ubuntu are basically the same.


![](6、Robot-development-environment-construction-in-Docker.pdf-1-1.jpeg)

![](6、Robot-development-environment-construction-in-Docker.pdf-1-2.jpeg)
#### 6.2.1、Remote configuration
See [VI. Linux Operating System---- 3. Remote Control] chapter


Make sure Windows can telnet to the Docker host [car]:


![](6、Robot-development-environment-construction-in-Docker.pdf-2-0.jpeg)


#### 6.2.2、vscode configuration
##### 6.2.2.1、download and install VSCODE
VSCODE official website: [https://code.visualstudio.com/, download the installation of the Windows](https://code.visualstudio.com/)

version

##### 6.2.2.2、vscode configuration ssh remote login to the host
1. Open vscode, click the icon of the arrow at the bottom left, then enter remote in the search box,

select the Remote Development plugin, and click Install to install the plugin


vscode is installed by default and then in English, and you can install Chinese plugins to localize:


2. Press the shortcut key [Ctrl + Shift + P] in VSCODE to open the command input window, type:

remote, and then log in to the remote host [car] according to the instructions shown below.


![](6、Robot-development-environment-construction-in-Docker.pdf-2-1.jpeg)

![](6、Robot-development-environment-construction-in-Docker.pdf-2-2.jpeg)
![](6、Robot-development-environment-construction-in-Docker.pdf-3-0.jpeg)

![](6、Robot-development-environment-construction-in-Docker.pdf-3-1.jpeg)

![](6、Robot-development-environment-construction-in-Docker.pdf-3-2.jpeg)

![](6、Robot-development-environment-construction-in-Docker.pdf-3-3.jpeg)

![](6、Robot-development-environment-construction-in-Docker.pdf-3-4.jpeg)

![](6、Robot-development-environment-construction-in-Docker.pdf-3-5.jpeg)
![](6、Robot-development-environment-construction-in-Docker.pdf-4-0.jpeg)

How to see the screen shown above, indicating that you have successfully logged in to the host

computer.

##### 6.2.2.3、enter the robot container
See the tutorial in the [5. Enter the docker container of the robot] chapter.

##### 6.2.2.4、Vscode remote host configuration docker environment
1. Install the docker plug-in on the remote host [car].


2. After the installation is completed, a docker icon will appear in the left navigation bar


![](6、Robot-development-environment-construction-in-Docker.pdf-5-0.jpeg)
![](6、Robot-development-environment-construction-in-Docker.pdf-6-0.jpeg)

3. Click the docker icon


![](6、Robot-development-environment-construction-in-Docker.pdf-7-0.jpeg)

4. Right-click the running container and operate as shown below:


![](6、Robot-development-environment-construction-in-Docker.pdf-8-0.jpeg)

![](6、Robot-development-environment-construction-in-Docker.pdf-8-1.jpeg)

5. A new window will open and see the following indicates that it has entered the container


6. Open the folder


![](6、Robot-development-environment-construction-in-Docker.pdf-8-2.jpeg)


![](6、Robot-development-environment-construction-in-Docker.pdf-9-0.jpeg)

![](6、Robot-development-environment-construction-in-Docker.pdf-9-1.jpeg)
![](6、Robot-development-environment-construction-in-Docker.pdf-10-0.jpeg)
![](6、Robot-development-environment-construction-in-Docker.pdf-11-0.jpeg)

7. Similarly, we can also install the plug-ins we need in the container to facilitate our development


![](6、Robot-development-environment-construction-in-Docker.pdf-12-0.jpeg)

In addition to ROS, the recommended plugins to install here are:


![](6、Robot-development-environment-construction-in-Docker.pdf-13-0.jpeg)

After completing the above steps, you can manipulate the code files in the container to develop and

learn.

##### 6.2.2.5、Configure passwordless login
In the above steps, some steps may require entering the password of the host, here is another

optimization, configure passwordless login.


1. First test using SSH to log in to the host [car] in Windows, the instructions are as follows:


At this time, you will find that you need to enter the host password


2. Next, configure password-free login


(1) Add environment variables


Open the environment variable properties page, click New in the user variables section, the variable is

HOME, the value is C:Usersname, where name is the user name, you can view the user name of your

own computer, and then the generated key pair is saved in this directory by default.


(2) Generate a key pair


Open the cmd command line, run it in the directory where the ssh program is located, or run [ssh
keygen -t rsa] anywhere after adding the system environment to generate the key, and then enter all

the way, when you see a histogram generated, then the key is generated successfully. At this time,

there will be two more files under the .ssh folder of the user directory, namely id_rsa (private key) and

id_rsa.pub (public key)


![](6、Robot-development-environment-construction-in-Docker.pdf-14-0.jpeg)
![](6、Robot-development-environment-construction-in-Docker.pdf-15-0.jpeg)

(3) Add the public key to the host


Similarly, open the cmd command line, enter


![](6、Robot-development-environment-construction-in-Docker.pdf-15-1.jpeg)


This command first logs in to the host, and then adds the public key under the local computer, i.e.

win, to the personal directory of the host account to achieve password-free login. Note that this step

requires the password of the host account.


(4) Verification


Test again using ssh in Windows to log in to the host [trolley], the command is as follows:


At this time, you will find that you no longer need to enter the password.


Restart VSCODE, and where you need to enter a password, you don't need to enter a password.
