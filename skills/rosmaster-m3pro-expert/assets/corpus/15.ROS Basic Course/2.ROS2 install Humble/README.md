# 2. Installing Humble in ROS2

- The ROS2-Humble installation supports Ubuntu 22.04.
- If you need to install a different version of ROS2, simply replace the **humble** version identifier in the installation command with the corresponding version. This applies to all other ROS-specific software in the ROS2 tutorial series and will not be covered in subsequent tutorials.

## 1. Set the locale

First, check whether the locale supports UTF-8 encoding. You can run the following command to check and set the UTF-8 encoding.

```
locale # Check for UTF-8 support
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
locale # Verify the configuration is successful
```

Note: The locale can be different, but must support UTF-8 encoding.

### 2. Set up the software source

Start the Ubuntu universe repository

```
sudo apt install software-properties-common
sudo add-apt-repository universe
```

Add the ROS 2 apt repository to the system and authorize our GPG key with apt.

```
sudo apt update && sudo apt install curl gnupg lsb-release -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o
/usr/share/keyrings/ros-archive-keyring.gpg
```

Add the repository to the source list

```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-
archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-
release && echo $UBUNTU_CODENAME) main" | sudo tee
/etc/apt/sources.list.d/ros2.list > /dev/null
```

# 3. Install Humble

First, update the apt repository cache:

```
sudo apt Update
```

Then upgrade the installed software (ROS2 packages are built on the frequently updated Ubuntu system. Please ensure your system is up to date before installing new packages):

```
sudo apt upgrade
```

Install the desktop version of ROS2 (recommended), which includes ROS, RViz, examples, and tutorials. The installation command is as follows. If you need to install a different version, replace "humble" in the command with the corresponding version number:

```
sudo apt install ros-humble-desktop python3-argcomplete
```

Install the colcon build tool

```
sudo apt install python3-colcon-common-extensions
```

### 4. Configure the Environment

If you are using a different version of ROS2, replace the "humble" version identifier with the corresponding version. For example, for the foxy version, replace "humble" with "foxy" in the command.

When executing ROS2 programs in a terminal, you need to run the following command to configure the environment:

```
source /opt/ros/humble/setup.bash
```

You must execute the above command each time you open a new terminal. Alternatively, you can run the following command to add the environment configuration instructions to the "~/.bashrc" file, eliminating the need to manually configure the environment each time you start a new terminal.

```
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

At this point, ROS2 has been installed and configured.

#### 5. Run the publisher and subscriber example nodes

The ROS2 desktop version has integrated some example nodes. You can test whether ROS2 is successfully installed by running these example nodes.

Run the publisher node

```
ros2 run demo_nodes_cpp talker
```

Run the subscriber node

```
ros2 run demo_nodes_cpp listener
```

### 6. Run and experience the turtle example

The turtle simulator, TurtleSim, is a classic teaching tool in ROS. It helps you quickly understand core ROS concepts.

Run the turtle simulator

```
ros2 run turtlesim turtlesim_node
```

Run the keyboard control node

```
ros2 run turtlesim turtle_teleop_key
```

View velocity topic data

```
ros2 topic echo /turtle1/cmd_vel
```

## 7. Uninstallation

After installing ROS2, if you want to uninstall it, you can execute the following command:

```
sudo apt remove ~nros-humble-* && sudo apt autoremove
```

You can also delete the ROS2 repository:

```
sudo rm /etc/apt/sources.list.d/ros2.list
sudo apt update
sudo apt autoremove
```
