# MoveIt2 Simulation Course

This section covers MoveIt2 configuration and simulation workflows for the ROSMASTER M3Pro robotic arm. It starts with generating a MoveIt2 configuration package, then demonstrates simulation-to-real-machine linkage, random motion, forward and inverse kinematics, Cartesian paths, trajectory visualization, collision avoidance, and scene-based object placement in RViz.

Use this section when you need to configure MoveIt2 for the M3Pro arm, test planned motion in RViz, or understand how MoveIt2 examples drive simulated and physical arm movement.

## [10.1 MoveIt2 Configuration](./1.MovelT2%20configuration/README.md)

Shows how to use MoveIt Setup Assistant to create a MoveIt2 configuration package for the M3Pro arm. The lesson covers loading the URDF, configuring self-collision detection, planning groups, robot poses, end effectors, ROS 2 controllers, MoveIt controllers, generated files, and basic Plan & Execute testing in RViz.

## [10.2 MoveIt2 Simulation-Reality Linkage](./2.MovelT2%20simulation-reality%20linkage/README.md)

Connects the simulated arm in RViz to the physical robotic arm. The lesson prepares the ROS agent and distributed communication, starts MoveIt2, runs the simulation-to-machine bridge, and shows how planned RViz motion is mirrored by the real arm.

## [10.3 Random Movement](./3.Random%20movement/README.md)

Demonstrates random target motion with MoveIt2. The program starts MoveIt2 in RViz, runs the random movement node, and plans the arm from a named pose to a randomly generated target pose.

## [10.4 Forward Kinematics Design](./4.Forward%20kinematics%20design/README.md)

Uses MoveIt2 to plan arm motion from specified joint values. The lesson sets target joint angles for `arm_group`, plans the motion, and executes the resulting trajectory in RViz.

## [10.5 Inverse Kinematics Design](./5.Inverse%20kinematics%20design/README.md)

Uses MoveIt2 to plan arm motion from a target end-effector pose. The program assigns a Cartesian pose to the arm, plans the required joint motion, and executes the plan in RViz.

## [10.6 Cartesian Path](./6.Cartesian%20path/README.md)

Plans a Cartesian end-effector path instead of a simple joint-space move. The lesson adds trajectory visualization in RViz, runs the Cartesian path example, and shows the generated green path points.

## [10.7 Trajectory Planning](./7.Trajectory%20planning/README.md)

Displays and executes planned trajectories in RViz. The lesson adds the trajectory display plugin, selects the relevant topics, and runs the multi-track motion example.

## [10.8 Collision Detection](./8.Collision%20detection/README.md)

Adds a collision object to the RViz planning scene and demonstrates obstacle-aware planning. The arm moves between named poses while MoveIt2 plans around the added obstacle.

## [10.9 Scene Design](./9.Scene%20design/README.md)

Builds a simple RViz scene with a three-layer shelf and a cylindrical object attached to the gripper. The program plans simulated placement motions to the middle shelf layers while avoiding published scene obstacles.
