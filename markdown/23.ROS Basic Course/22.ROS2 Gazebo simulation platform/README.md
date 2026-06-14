# 22. ROS2 Gazebo Simulation Platform
## 1. Introduction to Gazebo
Gazebo is the most commonly used 3D physics simulation platform in the ROS system. It supports

a dynamics engine and enables high-quality graphics rendering. It not only simulates the robot

and its surrounding environment, but also incorporates physical properties such as friction and

elasticity.


For example, if we want to develop a Mars rover, we can simulate the Martian surface

environment in Gazebo. Or, if we're developing a drone, battery life and flight restrictions prevent

us from frequently experimenting with the actual drone. In these cases, we can use Gazebo to

simulate first, then deploy to the actual drone once the algorithm is fully developed.


Simulation platforms like Gazebo can help us verify robotic algorithms, optimize robot designs,

and test robot applications, providing more possibilities for robotics development.


**Note: This section is for learning purposes only. The tutorial does not configure the**

**environment because we are using real-device debugging**
## 2. Installation and Operation
Install gazebo using the apt command


Run gazebo

Launch gazebo using the following command or directly from the desktop icon


![](22.ROS2-Gazebo-simulation-platform.pdf-0-2.jpeg)
![](22.ROS2-Gazebo-simulation-platform.pdf-1-0.jpeg)

After running, you should see the following page:


Optional: To ensure smooth model loading, you can download the offline model and place it

in the ~/.gazebo/models directory. The download link is as follows: https://github.com/osrf/g

azebo_models
## 3. Start the Gazebo Node and Service
1. View the Node


![](22.ROS2-Gazebo-simulation-platform.pdf-1-1.jpeg)


![](22.ROS2-Gazebo-simulation-platform.pdf-1-3.jpeg)

Correct return: /gazebo


2. View the external services provided by the node:


You can see the following results:


Excluding the last few regular services, we will only focus on the first three special services:


/spawn_entity, used to load models into gazebo

/get_model_list, used to obtain a model list

/delete_entity, used to delete loaded models in gazebo
## 4. Create a function package
Create a myrobot package to store our URDF model and launch files.


![](22.ROS2-Gazebo-simulation-platform.pdf-2-0.jpeg)


create a file called `demo01_base.urdf` . This file is a simple demonstration file containing only

a basic cube.


![](22.ROS2-Gazebo-simulation-platform.pdf-2-5.jpeg)


## 5. Writing the launch file
Writing a launch file consists of two main parts: launching the Gazebo file and then loading the

robot model into Gazebo.


![](22.ROS2-Gazebo-simulation-platform.pdf-3-0.jpeg)


This command starts Gazebo. It is a simple startup command and is not particularly complicated.

Here is the command to load the model:


![](22.ROS2-Gazebo-simulation-platform.pdf-3-1.jpeg)


Note the following two parameters in this command: -entity is the name of the model file, and
file is the parameter loaded through the urdf file. Later we can also see how the model is loaded

through the topic. Create a bringup_model.launch.py file in the launch directory. The complete

startup file is as follows:

```
 import os

 from launch import LaunchDescription

 from launch.actions import ExecuteProcess

 from launch_ros.actions import Node

 from launch_ros.substitutions import FindPackageShare

 from launch_ros.parameter_descriptions import ParameterValue

 from launch.substitutions import Command

 def generate_launch_description():

    robot_name_in_model = 'myrobot'

    package_name = 'myrobot'

    urdf_name = "demo01_base.urdf"

    ld = LaunchDescription()

    pkg_share = FindPackageShare(package=package_name).find(package_name)

    urdf_model_path = os.path.join(pkg_share, f'urdf/{urdf_name}')

    # Start Gazebo server

    start_gazebo_cmd = ExecuteProcess(

      cmd=['gazebo', '--verbose','-s', 'libgazebo_ros_init.so', '-s',

 'libgazebo_ros_factory.so'],

      output='screen')

    # Launch the robot

    spawn_entity_cmd = Node(

      package='gazebo_ros',

      executable='spawn_entity.py',

      arguments=['-entity', robot_name_in_model, '-file', urdf_model_path ],

 output='screen')

    ld.add_action(start_gazebo_cmd)

```

```
  ld.add_action(spawn_entity_cmd)

  return ld

```

Fill in the following content in Cmakelist to install our urdf and launch folders into the install

directory


![](22.ROS2-Gazebo-simulation-platform.pdf-4-0.jpeg)


Then compile and run the function package


![](22.ROS2-Gazebo-simulation-platform.pdf-4-2.jpeg)

Refresh the environment variables and run the launch startup file


![](22.ROS2-Gazebo-simulation-platform.pdf-4-4.jpeg)

After launching, you should see the following Gazebo model:


![](22.ROS2-Gazebo-simulation-platform.pdf-5-0.jpeg)

You can see the red model because you added the Gazebo tag settings.
