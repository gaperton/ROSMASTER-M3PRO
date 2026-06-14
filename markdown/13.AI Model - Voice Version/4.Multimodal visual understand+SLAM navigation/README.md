# Multimodal Visual Understanding + SLAM Navigation
**Multimodal Visual Understanding + SLAM Navigation**

1. Course Content

2. Preparation

### 2.1 Content Description

### 2.2 Starting the Agent

### 2.3 Configuring the Map Mapping File

3. Running Example

### 3.1 Starting the Program

### 3.2 Test Cases

4. Source Code Analysis

## 1. Course Content
Basic: Run example programs, combining the robot's visual understanding capabilities with

SLAM navigation for integrated tasks.

Advanced: Master the key source code introduced in this section.
## 2. Preparation
### 2.1 Content Description
This section of the course uses the Jetson Orin NX as an example. For Raspberry Pi and Jetson

Nano boards, you need to open a terminal on the host machine, then enter the command to

enter the Docker container. After entering the Docker container, enter the commands mentioned

in this section of the course in the terminal. Instructions on how to access the Docker container

from the host machine can be found in the product tutorial [0. Instructions and Installation Steps],

specifically the section [Accessing the Robot's Docker (For Jetson Nano and Raspberry Pi 5 users)].

For Orin and NX boards, simply open a terminal and enter the commands mentioned in this

section.

### 2.2 Starting the Agent
**Note: If the agent is already running, there is no need to start it again.**


Enter the following command in the vehicle terminal:


The terminal will print the following information, indicating a successful connection:


![](Multimodal-visual-understand+SLAM-navigation.pdf-1-0.jpeg)


[!NOTE]


Note: To experience this section, you need to have built at least one grid map according to

the LiDAR section of the course.

### 2.3 Configuring the Map Mapping File
Connect to the robot's desktop via VNC and start the navigation node using the following

commands:


Start rviz on the robot:


Alternatively, you can start the display on the virtual machine; there is no need to start the

display window repeatedly.


## Afterward, the rviz2 visualization interface will open. Click 2D Pose Estimate in the toolbar above

to enter the selection state, and roughly mark the robot's position and orientation on the map.


The robot model will be displayed in the map, as shown below:


![](Multimodal-visual-understand+SLAM-navigation.pdf-2-0.jpeg)

We can name any precise point on the map. Here, we use "Master Bedroom" and "Kitchen" as

examples.


As shown in the figure below, we first click the **Nav2 Goal** tool to navigate the robot to the target

point we need to mark.


![](Multimodal-visual-understand+SLAM-navigation.pdf-2-1.jpeg)
![](Multimodal-visual-understand+SLAM-navigation.pdf-3-0.jpeg)

![](Multimodal-visual-understand+SLAM-navigation.pdf-3-1.jpeg)

Run the following command in the terminal to obtain the current robot's pose information in

the map coordinate system:


![](Multimodal-visual-understand+SLAM-navigation.pdf-4-0.jpeg)

Open the `map_mapping.yaml` map mapping file (you can open it using VNC, VS Code, command

line, or any other method):


Here's an example of opening the file via the command line:


![](Multimodal-visual-understand+SLAM-navigation.pdf-4-2.jpeg)

in the previously obtained pose information into the `position` and `orientation` fields.

```
# 根据实际的场景环境，自定义地图中的区域，可以添加任意个区域，注意和大模型的地图映射保持一致即可

#According to the actual scene environment, customize the areas in the map. You

can add any number of areas, just make sure they are consistent with the map

mapping of the large model
# 地图映射 Map mapping

common_map_areas: # 常规导航 common navigation

A:

name: 'Master Bedroom'

position:

x: 3.974

y: -2.634

orientation:

x: 0.0

y: 0.0

z: -0.688

```

```
 w: 0.726

 B:

 name: 'xxx'

 position:

 x: 1.488

 y: 0.661

 z: 0.0

 orientation:

 x: 0.0

 y: 0.0

 z: 0.725

 w: 0.688

```

After the modifications are complete, saving the file will take effect immediately. 2.4 Configuring

Map Mapping Variables in Dify


After configuring the map mapping file as described above, we need to let the AI large

language model know the relationship between the locations and symbols in these maps.

Start the Dify service (if already started, no need to restart):


![](Multimodal-visual-understand+SLAM-navigation.pdf-5-1.jpeg)

Enter the vehicle's IP address directly in the browser's address bar to access the Dify

management page, then click to select the corresponding AI application.


[!NOTE]


International users: multi_brains_en


![](Multimodal-visual-understand+SLAM-navigation.pdf-5-2.jpeg)
![](Multimodal-visual-understand+SLAM-navigation.pdf-6-0.jpeg)

the settings in the previous map mapping file, and then click Save.


Finally, remember to click Publish -> Publish Update to save the changes.


![](Multimodal-visual-understand+SLAM-navigation.pdf-6-2.jpeg)
![](Multimodal-visual-understand+SLAM-navigation.pdf-7-0.jpeg)
## 3. Running Example
### 3.1 Starting the Program
On the vehicle's terminal, enter the command to start the AI intelligent agent system:


Or you can use the shortcut command:


Start the navigation command on the vehicle's onboard computer:


Start rviz on the robot:


Then, follow the procedure for starting the navigation function to initialize the positioning.
## This will open the rviz2 visualization interface. Click on 2D Pose Estimate in the toolbar

above to enter the selection state. Mark the approximate position and orientation of the

robot on the map. After initializing the positioning, the preparation work is complete.


![](Multimodal-visual-understand+SLAM-navigation.pdf-8-5.jpeg)
### 3.2 Test Cases
The cases are for reference only; provide instructions according to your needs. - Please remember

your current location first, then navigate to the kitchen and the master bedroom in sequence,

remembering the items you see. Finally, return to your starting position and tell me what you saw

in those two places?


Wake up the robot and issue commands. The execution layer large model will execute

subtasks according to the task steps planned by the decision layer model: 1. Navigate to the

"master bedroom," then observe the items in the environment. Place a pen in the simulated

"master bedroom," and place a pack of toilet paper in the simulated "kitchen":


The robot executes the steps according to the output process of the decision layer as

follows:

## 4. Source Code Analysis
Robot action source code path:


![](Multimodal-visual-understand+SLAM-navigation.pdf-9-0.jpeg)

![](Multimodal-visual-understand+SLAM-navigation.pdf-9-1.jpeg)
action_service.py program:


**Understanding + Robotic Arm Grasping** section. This section explains the newly introduced


Creates a nav2 navigation client to request the ros2 navigation action server for subsequent

sending of navigation target point requests; creates a TF listener to listen to the coordinate

transformation between map and base_footprint.


![](Multimodal-visual-understand+SLAM-navigation.pdf-10-9.jpeg)


**load_target_points** function:


This function is responsible for loading the target point coordinates from the

`map_mapping.yaml` map mapping file and creating a navigation dictionary to store

characters and their corresponding map coordinates. Each point coordinate is of type

PoseStamped.


![](Multimodal-visual-understand+SLAM-navigation.pdf-10-10.jpeg)


**_normal_navigation** function:


Receives a character parameter (corresponding to the characters in the map mapping

described above), parses the coordinates corresponding to that character from the


navigation action server. When the navigation action server returns a value of 4, it indicates

successful navigation; other values indicate failure (possibly due to obstacles, planning

failures, etc.). After the navigation is complete, the function provides feedback on the action

execution result to the large language model.

```
  def __normal_navigation(self, point_name)->None:
     ''' 常规导航功能 / Normal navigation function '''

     self.navigation_finish_flag = False

     self.goal_handle = None

     self.result = None

     self.res = None

     point_name = point_name.strip("'\"")

     if point_name not in self.navpose_dict:

       self.get_logger().error(f"Target point '{point_name}' does not exist

in the navigation dictionary." )

       return None

     if self.first_record:
       # 出发前记录当前在全局地图中的坐标 ( 只有在每个任务周期的第一次执行时才会记录 )/

before starting a new task, record the current pose in the global map

       transform = self.tf_buffer.lookup_transform(

          "map", "base_footprint", rclpy.time.Time()

)

       pose = PoseStamped()

       pose.header.frame_id = "map"

       pose.pose.position.x = transform.transform.translation.x

       pose.pose.position.y = transform.transform.translation.y

       pose.pose.position.z = 0.0

       pose.pose.orientation = transform.transform.rotation

       self.navpose_dict["zero"] = pose

       self.road_net_dict["zero"] = pose

       self.first_record = False

     # 获取目标点坐标 /get_target_pose

     target_pose = self.navpose_dict.get(point_name)

     goal_msg = NavigateToPose.Goal()

     goal_msg.pose = target_pose

     send_goal_future = self.navclient.send_goal_async(goal_msg)

     def goal_response_callback(future):

       self.goal_handle = future.result()

       if not self.goal_handle or not self.goal_handle.accepted:

          self.get_logger().error("Goal was rejected!")

          return None

       get_result_future = self.goal_handle.get_result_async()

       def result_callback(future_result):

          self.result = future_result.result()

          self.navigation_finish_flag = True

          if self.result.status == 4:

            self.get_logger().info("Navigation finished!")

            self.res= True

```

```
           else:

             self.get_logger().info(f"Navigation failed with status:

 {self.result.status}")

             self.res= False

        get_result_future.add_done_callback(result_callback)

      send_goal_future.add_done_callback(goal_response_callback)

      while not self.navigation_finish_flag:

        if self.interrupt_event.is_set() :

           self.navclient._cancel_goal(self.goal_handle)

           return None

        time.sleep(0.1)

      self.stop()

      return self.res

```

The **get_current_pose** function retrieves the robot's current map coordinates in the global

coordinate system and stores these coordinates in a dictionary for easy retrieval later.


![](Multimodal-visual-understand+SLAM-navigation.pdf-12-0.jpeg)
