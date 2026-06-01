# Forward Kinematics Design

Raspberry Pi 5 and Jetson Nano run ROS in Docker, so MoveIt2 performance is usually limited on those boards. Raspberry Pi 5 and Jetson Nano users should run these MoveIt2 examples in the virtual machine. Orin users can run the same commands directly on the robot because ROS runs directly on the Orin mainboard.

This lesson uses the virtual machine as the example environment.

## 1. Content Description

This lesson uses MoveIt2 to plan arm motion from specified joint angles. Forward kinematics calculates the end-effector pose from the robotic arm's joint values. In RViz, the program sets target joint angles and asks MoveIt2 to plan and execute the corresponding motion.

## 2. Program Startup

Open a terminal in the virtual machine and start MoveIt2:

```bash
ros2 launch test_moveit_config demo.launch.py
```

When the terminal displays **"You can start planning now!"**, MoveIt2 has started successfully.

![Figure: page 0: figure 9](_page_0_Figure_9.jpeg)

Start the forward-kinematics example:

```bash
ros2 run MoveIt_demo set_target_joints
```

After the program starts, the robotic arm in RViz plans a motion to the configured joint posture.

![Picture: page 1: picture 1](_page_1_Picture_1.jpeg)

## 3. Core Code Analysis

Program code path in the virtual machine:

```text
/home/yahboom/moveit2_ws/src/MoveIt_demo/src/set_target_joints.cpp
```

```python
#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <vector>
class RandomMoveIt2Control : public rclcpp::Node
{
public:
  RandomMoveIt2Control()
    : Node("random_moveit2_control")
  {
    RCLCPP_INFO(this->get_logger(), "Initializing RandomMoveIt2Control.");
  }
  void initialize()
  {
    int max_attempts = 5 ; // Maximum number of planning attempts
    int attempt_count = 0 ; // Current number of attempts
    //Initialize move_group_interface_ in this function and create a planning
group named arm_group
    move_group_interface_ =
std::make_shared<moveit::planning_interface::MoveGroupInterface>
(shared_from_this(), "arm_group");
    //The following is the setting for the planning group
    move_group_interface _-> setNumPlanningAttempts ( 10 ); // Set the maximum
number of planning attempts to 10
```

```
move_group_interface _-> setPlanningTime ( 5.0 ); // Set the
maximum time for each planning to 5 seconds
    move_group_interface _-> allowReplanning ( true ); //Allow replanning after
failure
    move_group_interface _-> setReplanAttempts ( 5 ); //Run replanning 5 times
    while (attempt_count < max_attempts)
    {
        attempt_count++;
        std::vector < double > target_joints = { 0 , - 0.69 , - 0.17 , 0.86 ,
0 }; // Target joint angles (unit: radians)
        // Set the target joint space value setJointValueTarget
        move_group_interface_->setJointValueTarget(target_joints);
        // Initialize plan
        moveit::planning_interface::MoveGroupInterface::Plan my_plan;
        //Execute plan plan(my_plan)
        bool success = (move_group_interface_->plan(my_plan) ==
moveit::core::MoveItErrorCode::SUCCESS);
        if (success)
        {
            //If the plan is successful, execute the plan, execute(my_plan)
            RCLCPP_INFO(this->get_logger(), "Planning succeeded, moving the
arm.");
            move_group_interface_->execute(my_plan);
            return;
        }
        else
        {
            RCLCPP_ERROR(this->get_logger(), "Planning failed!");
        }
    }
    RCLCPP_ERROR(this->get_logger(), "Exit!");
  }
private:
  std::shared_ptr<moveit::planning_interface::MoveGroupInterface>
move_group_interface_;
};
int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<RandomMoveIt2Control>();
  // Delayed initialization
  node->initialize();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
```
