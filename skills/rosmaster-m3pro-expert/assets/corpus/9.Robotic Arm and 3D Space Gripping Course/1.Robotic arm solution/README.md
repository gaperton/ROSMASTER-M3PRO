# Robotic Arm Solution

## 1. Content Description

This lesson introduces the robotic arm's forward-kinematics and inverse-kinematics calculations. Forward kinematics calculates the end-effector pose from the servo angles. Inverse kinematics calculates the servo angles needed to reach a target end-effector pose.

Both calculations are important for 3D grasping. Forward kinematics provides the current end-effector pose for coordinate transforms. Inverse kinematics calculates the servo targets that move the gripper to the grasping pose before the arm clamps an object.

This lesson requires terminal commands. Use the terminal that matches your mainboard. Raspberry Pi 5 and Jetson Nano users should open a terminal on the host system, enter the Docker container, and then run the commands from this lesson inside the container. For Docker entry steps, see **Configuration and Operation Guide - Enter the Docker (Jetson Nano and Raspberry Pi 5 users, see here)**.

Orin users can open a terminal directly on the robot and run the commands there.

## 2. Program Startup

Start the arm kinematics node:

```bash
ros2 run arm_kin kin_srv
```

After startup, run `ros2 node list` in the terminal to view the node list.

`/kinemarics_arm` is the node that provides the forward- and inverse-kinematics service. Run `ros2 node info /kinemarics_arm` to inspect the node.

As shown above, `/kinemarics_arm` provides the `/get_kinemarics` service. Its service type is `arm_interface/srv/ArmKinemarics`. Run `ros2 interface show arm_interface/srv/ArmKinemarics` to view the request and response fields.

```
float64 tar_x
float64 tar_y
float64 tar_z
float64 roll
float64 pitch
float64 yaw
float64 cur_joint1
float64 cur_joint2
float64 cur_joint3
float64 cur_joint4
float64 cur_joint5
float64 cur_joint6
string kin_name
---
float64 joint1
float64 joint2
float64 joint3
float64 joint4
float64 joint5
float64 joint6
float64 x
float64 y
float64 z
float64 roll
float64 pitch
float64 yaw
```

The service data is divided into request and response sections. The request fields are:

```
#The x coordinate of the end position of the robotic arm, in meters
float64 tar_x
#The y coordinate of the end position of the robotic arm, in meters
float64 tar_y
#The z coordinate of the end position of the robotic arm, in meters
float64 tar_z
```

```
#Rotation value of the end-arm posture roll around the X-axis, in radians
float64 roll
#Rotation value of the pitch value of the end arm around the y-axis, in radians
float64 pitch
#The yaw value of the end position of the robot arm is the rotation value around
the z axis, in radians
float64 yaw
#Current value of Servo No. 1, in degrees
float64 cur_joint1
#Current value of Servo 2, in degrees
float64 cur_joint2
#Current value of Servo 3, in degrees
float64 cur_joint3
#Current value of Servo 4, in degrees
float64 cur_joint4
#Current value of servo No. 5, unit is degree
float64 cur_joint5
#Current value of servo No. 6, unit is degree
float64 cur_joint6
#Solution type: ik represents inverse kinematics solution, fk represents forward
kinematics solution
string kin_name
```

The response fields are:

```
#1 Servo Angle
float64 joint1
#2 Servo Angle
float64 joint2
#3 Servo Angle
float64 joint3
#4 Servo Angle
float64 joint4
#5 Servo Angle
float64 joint5
#6 Servo Angle
float64 joint6
#x coordinate of the end pose of the robotic arm
float64 x
#The end pose coordinates of the robotic arm
float64 y
#z coordinate of the end position of the robotic arm
float64 z
#Rotation value of the end-arm posture roll around the X-axis, in radians
float64 roll
#Rotation value of the pitch value of the end arm around the Y axis, in radians
float64 pitch
#The yaw value of the end-arm position is the rotation value around the Z axis,
in radians
float64 yaw
```

### 2.1. Call FK

Call `fk` to calculate the end-effector pose when the robotic arm is straightened upward. After the agent connects successfully, run the following command to move the arm to the upright pose:

```bash
ros2 topic pub /arm6_joints arm_msgs/msg/ArmJoints { "joint1: 90,joint2:
90,joint3: 90,joint4: 90,joint5: 90,joint6: 90,time: 1500" } --once
```

After the arm straightens upward, call the `fk` service:

```
ros2 service call /get_kinemarics arm_interface/srv/ArmKinemarics "{tar_x: 0.0,
tar_y: 0.0, tar_z: 0.0, roll: 0.0, pitch: 0.0, yaw: 0.0, cur_joint1: 90.0,
cur_joint2: 90.0, cur_joint3: 90.0, cur_joint4: 90.0, cur_joint5: 90.0,
cur_joint6: 90.0, kin_name: 'fk'}"
```

Set `cur_joint1` through `cur_joint6` to `90.0`. Set `kin_name` to `fk` to call the forward-kinematics service. The terminal returns a response like the one shown below.

Check the response section:

```
response:
arm_interface.srv.ArmKinemarics_Response (joint1 = 0 .0, joint2 = 0 .0, joint3 =
0 .0, joint4 = 0 .0, joint5 = 0 .0, joint6 = 0 .0, x = 0 .03141308752246765, y =
0 .00020942581836905875, z = 0 .5517500187814817, roll = 1 .5728637148906415,
pitch = -1 .5707324948694676, yaw = -1 .5728927150075942)
```

Focus on the `x`, `y`, `z`, `roll`, `pitch`, and `yaw` values. These values describe the end-effector pose in the world coordinate system, using `base_link` at `(0, 0, 0)` as the reference. With the arm straightened upward, the example pose is `x=0.03141308752246765`, `y=0.00020942581836905875`, `z=0.5517500187814817`, `roll=1.5728637148906415`, `pitch=-1.5707324948694676`, and `yaw=-1.5728927150075942`. To compare this with the URDF visualization, start the URDF display in the virtual-machine terminal:

```bash
ros2 launch yahboom_M3Pro_description display_launch.py
```

As shown below, the TF plugin can display the `Gripping` pose. The `xyz` values are almost the same as the service response. The `rpy` values are obtained by converting the displayed quaternion to roll, pitch, and yaw.

![Figure: page 4: figure 0](_page_4_Figure_0.jpeg)

### 2.2. Call IK

Call `ik` to calculate the servo angles for the same end-effector pose: `x=0.03141308752246765`, `y=0.00020942581836905875`, `z=0.5517500187814817`, `roll=1.5728637148906415`, `pitch=-1.5707324948694676`, and `yaw=-1.5728927150075942`. Because this is the pose produced by all joints at `90.0`, the inverse-kinematics result should return approximately the same servo values. Run:

```
ros2 service call /get_kinemarics arm_interface/srv/ArmKinemarics "{tar_x:
0.03141308752246765, tar_y: 0.00020942581836905875, tar_z: 0.5517500187814817,
roll: 1.5728637148906415, pitch: -1.5707324948694676, yaw: -1.5728927150075942,
cur_joint1: 0.0, cur_joint2: 0.0, cur_joint3: 0.0, cur_joint4: 0.0, cur_joint5:
0.0, cur_joint6: 0.0, kin_name: 'ik'}"
```

Here, the important inputs are `xyz` and `rpy`; `cur_joint1` through `cur_joint6` can use their default values. The result is shown below.

The final response is:

```
arm_interface.srv.ArmKinemarics_Response(joint1=90.0, joint2=90.0, joint3=90.0,
joint4=90.0, joint5=90.0, joint6=0.0, x=0.0, y=0.0, z=0.0, roll=0.0, pitch=0.0,
yaw=0.0)
```

Focus on `joint1` through `joint5`. Because the gripper is connected after servo No. 5, servo No. 6 is not part of this inverse-kinematics solution. The returned values, `[90.0, 90.0, 90.0, 90.0, 90.0]`, match the current arm posture, so the inverse-kinematics result is correct for this example.

## 3. Core Code Analysis

Program code path:

Raspberry Pi 5 and Jetson Nano:

```text
/root/yahboomcar_ws/src/arm_kin/src/kin_srv.cpp
```

Orin:

```text
/home/jetson/yahboomcar_ws/src/arm_kin/src/kin_srv.cpp
```

Main function:

```
int main ( int argc , char ** argv )
{
   rclcpp::init ( argc , argv );
   rcutils_logging_set_logger_level ( "kdl_parser" , RCUTILS_LOG_SEVERITY_ERROR
);
   auto node = rclcpp::Node::make_shared ( "kinemarics_arm" );
   //Create a service with the service name get_kinemarics and the service
callback function handle_service
   auto service = node -> create_service < arm_interface::srv::ArmKinemarics
> ( "get_kinemarics" , handle_service );
   rclcpp::spin ( node );
   rclcpp::shutdown ();
   return 0 ;
}
```

The `handle_service` callback processes kinematics service requests:

```
void handle_service (
 const std::shared_ptr < arm_interface::srv::ArmKinemarics::Request > request
,
 std::shared_ptr < arm_interface::srv::ArmKinemarics::Response > response )
{
 cout << "-----------------" << endl ;
 cout << request -> kin_name << endl ;
     if ( request -> kin_name == "fk" ) {
       double joints []{ request -> cur_joint1 , request -> cur_joint2 ,
request -> cur_joint3 , request -> cur_joint4 ,
                       request -> cur_joint5 , request -> cur_joint6 };
       // Define the target joint angle container
       vector < double > initjoints ;
       // Define pose container
       vector < double > initpos ;
       // Target joint angle unit conversion, from degrees to radians
       for ( int i = 0 ; i < 6 ; ++ i ) initjoints . push_back (( joints [
i ] - 90 ) * DE2RA );
       //Call fk to get the target pose initpos
       arm_getFK ( urdf_file , initjoints , initpos );
       response -> x = initpos . at ( 0 );
       response -> y = initpos . at ( 1 );
       response -> z = initpos . at ( 2 );
       response -> roll = initpos . at ( 3 );
```

```
response -> pitch = initpos . at ( 4 );
       response -> yaw = initpos . at ( 5 );
       cout << "-----------------" << endl ;
   }
   if ( request -> kin_name == "ik" ) {
       // Grasping pose
       double Roll = request -> roll ;
       double Pitch = request -> pitch ;
       double Yaw = request- > yaw ;
       double x = request -> tar_x ;
       double y = request- > tar_y ;
       double z = request -> tar_z ;
       // End position (unit: m)
       double xyz []{ x , y , z };
       cout << x << y << z << endl ;
       // End attitude (unit: radians)
       //double rpy[]{Roll * DE2RA, Pitch * DE2RA, Yaw * DE2RA};
       double rpy []{ Roll , Pitch , Yaw };
       // Create output angle container
       vector < double > outjoints ;
       // Create the end position container
       vector < double > targetXYZ ;
       // Create an end gesture container
       vector < double > targetRPY ;
       for ( int k = 0 ; k < 3 ; ++ k ) targetXYZ . push_back ( xyz [ k
]);
       for ( int l = 0 ; l < 3 ; ++ l ) targetRPY . push_back ( rpy [ l
]);
       // //Call fk to get the target servo angle outjoints
       arm_getIK ( urdf_file , targetXYZ , targetRPY , outjoints );
       // Print the inverse solution
       for ( int i = 0 ; i < 5 ; i ++ ) cout << ( outjoints . at ( i ) *
RA2DE ) + 90 << "," ;
       cout << endl ;
       a ++ ;
       response -> joint1 = ( outjoints . at ( 0 ) * RA2DE ) + 90 ;
       response -> joint2 = ( outjoints . at ( 1 ) * RA2DE ) + 90 ;
       response -> joint3 = ( outjoints . at ( 2 ) * RA2DE ) + 90 ;
       response -> joint4 = ( outjoints . at ( 3 ) * RA2DE ) + 90 ;
       response -> joint5 = ( outjoints . at ( 4 ) * RA2DE ) + 90 ;
       cout << "-----------------" << endl ;
   }
}
```
