# Install and Start the micro-ROS Agent

## 1. Start the micro-ROS Agent with Docker

### Start the Serial-Port Agent

```bash
docker run -it --rm -v /dev:/dev -v /dev/shm:/dev/shm --privileged --net=host microros/micro-ros-agent:humble serial --dev /dev/myserial -b 2000000 -v4
```

Here, `--dev /dev/myserial` is the bound serial-port device. You can change it to another device, such as `/dev/ttyUSB0`, if needed.

`-b 2000000` sets the baud rate.

To exit the agent, press `Ctrl+C` in the terminal.

Do not close the terminal window directly, or Docker may continue running in the background.

If the MCU reconnects to the agent several times, ROS 2 may discover multiple identical nodes. This does not affect normal use. Press `Ctrl+C` to stop the agent, then reset the MCU so it reconnects cleanly.

#### Agent startup failure

The micro-ROS agent can run in only one terminal at a time. If another terminal has already started the agent in the background, starting it again reports an error. Press `Ctrl+C` in the original agent terminal before running the agent again.

If the agent fails to start because the terminal was closed directly, restart the virtual machine or computer, or stop the Docker container manually.

To stop Docker manually, first query the current Docker process, then stop the current agent container.


```bash
docker ps -a | grep microros/micro-ros-agent
docker stop xxxxxxxxxx
```

## 2. Start the micro-ROS Agent from Source

### Install tinyxml2 dependencies

Run the following commands in the terminal to install `tinyxml2`:

```bash
cd ~/
git clone https://github.com/leethomason/tinyxml2.git
cd tinyxml2
mkdir build
cd build
sudo cmake ..
sudo make
sudo make install
```

#### Install the python3-rosdep tool

Run the following command to install `rosdep`. If it is already installed, skip this step.

```bash
sudo apt install python3-rosdep
```

### Build the `micro_ros_setup` Environment

Activate the ROS 2 environment variables. This example uses Humble. If the environment is already active, skip this step.

```bash
source /opt/ros/humble/setup.bash
```

Create and enter the `uros_ws` workspace in the user directory:

```bash
mkdir ~/uros_ws && cd ~/uros_ws
mkdir src
```

Download `micro_ros_setup` into the `src` folder:

```bash
git clone -b $ROS_DISTRO https://github.com/micro-ROS/micro_ros_setup.git
src/micro_ros_setup
```

Initialize `rosdep`:

```
sudo rosdep init
```

```
sudo -E rosdep init
```

If both commands return errors and `rosdep` still cannot be initialized, create `/etc/ros/rosdep/sources.list.d/20-default.list`, add the following content, then continue to the next step.

```
# os-specific listings first
yaml https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/osx-
homebrew.yaml osx
# generic
yaml https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/base.yaml
yaml https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/python.yaml
yaml https://raw.githubusercontent.com/ros/rosdistro/master/rosdep/ruby.yaml
gbpdistro
https://raw.githubusercontent.com/ros/rosdistro/master/releases/fuerte.yaml
fuerte
# newer distributions (Groovy, Hydro, ...) must not be listed anymore, they are
being fetched from the rosdistro index.yaml instead
```

Update `rosdep` and install the required packages:

```
rosdep update && rosdep install --from-paths src --ignore-src -y
```

Build the workspace:

```bash
colcon build
```

```bash
source install/local_setup.bash
```

#### Build the `micro_ros_agent` Environment

```bash
ros2 run micro_ros_setup create_agent_ws.sh
ros2 run micro_ros_setup build_agent.sh
```

If `build_agent.sh` reports an error, run the build command again.

### Start the micro-ROS Serial-Port Agent from Source

Activate the `micro_ros_agent` environment:

```bash
source ~/uros_ws/install/local_setup.sh
```

Start the serial-port agent from the ROS 2 environment:

```bash
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/myserial -b 2000000
-v4
```

Here, `--dev /dev/myserial` is the bound serial-port device. You can change it to another device, such as `/dev/ttyUSB0`, if needed.

`-b 2000000` sets the baud rate.

To exit the agent, press `Ctrl+C` in the terminal.

## 3. Start the micro-ROS agent with the factory image

The factory image includes the agent script. Run the following command to start the agent:

```bash
sh ~/start_agent.sh
```
