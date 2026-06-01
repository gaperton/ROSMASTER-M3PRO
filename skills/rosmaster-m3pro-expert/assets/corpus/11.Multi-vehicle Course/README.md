# Multi-Vehicle Course

This section covers coordinated operation with multiple ROSMASTER robots. It starts with the shared setup required for robots on the same ROS 2 network, then shows how to control multiple chassis, control multiple robotic arms, run multi-robot navigation, and maintain a three-robot formation.

## [11.1 Multi-Vehicle Chassis Control](./1.Multi-vehicle%20chassis%20control/README.md)

Use a keyboard node in the virtual machine to publish velocity commands that multiple robots receive through their own namespaces. This lesson also explains the shared ROS_DOMAIN_ID, LAN, and namespace setup used by the rest of the multi-vehicle course.

## [11.2 Multi-Vehicle Robotic Arm Control](./2.Multi-vehicle%20robotic%20arm%20control/README.md)

Connect the gamepad receiver to the virtual machine, start the joystick and ROSMASTER control nodes, and use the controller to command the chassis and robotic arms on multiple robots.

## [11.3 Multi-Vehicle Navigation](./3.Multi-vehicle%20navigation/README.md)

Run two robots on the same map with separate AMCL and Nav2 instances. RViz provides separate initial-pose and goal tools so each robot can localize, plan, avoid obstacles, and navigate to its own target.

## [11.4 Multi-Vehicle Formation](./4.Multi-vehicle%20formation/README.md)

Arrange three robots into a programmed formation. Robot1 acts as the lead robot, publishes follower target transforms, and robot2 and robot3 navigate to those generated points to maintain the selected formation.
