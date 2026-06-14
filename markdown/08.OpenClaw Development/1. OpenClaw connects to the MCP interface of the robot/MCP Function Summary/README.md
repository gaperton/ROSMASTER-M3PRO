# ROSMASTER-M3Pro-MCP Feature Summary
**ROSMASTER-M3Pro-MCP Feature Summary**

Feature Overview

Detailed Function Descriptions

1. MoveWithSpeed

2. Move

3. GetCurrentArmJointAngles

4. GetEndEffectorPose

5. ControlSixArmJoint

6. ControlSingleArmJoint

7. Place


8. Pick

9. AdjustCameraView

10. SeeWhat

11. InitArmPose

12. GetBbox

13. GetPlacePoint

14. AdjustChassisFitArmRange

15. RecordMapLocation

16. GetMapMapping

17. Navigation

18. GetWasteRecognitionResults

19. GraspWaste

20. PlaceWaste

21. TTS

22. Rotate

23. TargetTrack

24. GetTargetDist

25. GraspArUcoTarget

26. GetAprilTagIDs

27. FollowLine

Function Categories

Chassis Control

Robotic Arm Control

Grasping Operations

Vision Functions

Mapping & Navigation

Speech Synthesis


quickly understand the function, parameters, and usage of each tool.

**Feature Overview**


|No.|Tool Name|Function Description|
|---|---|---|
|1|MoveWithSpeed|Control the robot's omnidirectional chassis speed|
|2|Move|Control the robot chassis to move a specified<br>distance|
|3|GetCurrentArmJointAngles|Retrieve the robotic arm's current joint angles|
|4|GetEndEffectorPose|Retrieve the end-effector's pose|
|5|ControlSixArmJoint|Simultaneously control the arm's 6 joints|
|6|ControlSingleArmJoint|Control a single arm joint to a specified angle|
|7|Place|Place an object at specified coordinates|
|8|Pick|Grasp an object|
|9|AdjustCameraView|Adjust the camera's viewpoint|
|10|SeeWhat|Capture a camera image and return the save path|
|11|InitArmPose|Restore the arm to its preset initial pose|
|12|GetBbox|Detect the bounding box coordinates of a target<br>object|
|13|GetPlacePoint|Retrieve placement point coordinates and check<br>reachability|
|14|AdjustChassisFitArmRange|Quickly adjust the chassis so the target point is<br>within the arm's workspace|
|15|RecordMapLocation|Save the current location to a map mapping file|
|16|GetMapMapping|Retrieve the mapping relationship between location<br>names and symbols|
|17|Navigation|Navigate to a specified location using a target<br>symbol|
|18|GetWasteRecognitionResults|Retrieve waste recognition results from the YOLO<br>model|
|19|GraspWaste|Grasp a waste object|
|20|PlaceWaste|Place a waste object|
|21|TTS|Robot speech synthesis|
|22|Rotate|Rotate in place by a specified angle|
|23|TargetTrack|Visually track a target object|
|24|GetTargetDist|Calculate the distance between the target and the<br>robot chassis|
|25|GraspArUcoTarget|Grasp an AprilTag target with a specified ID|


|No.|Tool Name|Function Description|
|---|---|---|
|26|GetAprilTagIDs|Retrieve AprilTag IDs within the field of view|
|27|FollowLine|Follow a line of a specified color|


**Detailed Function Descriptions**
## 1. MoveWithSpeed
**Function** : Controls the robot's omnidirectional chassis movement using velocity commands.


**Parameters** :


**Return Value** : `common_response`

## 2. Move
**Function** : Controls the robot's chassis to move a specified distance.


**Parameters** :


`'right'` : Move laterally to the right


**Return Value** : `common_response`

## 3. GetCurrentArmJointAngles
**Function** : Retrieves the current joint angles of the robotic arm.


**Parameters** : None


`gripper` : Gripper angle.

## 4. GetEndEffectorPose
**Function** : Retrieves the pose (position and orientation) of the end effector (comprising the

gripper and camera).


**Parameters** : None


**Return Value** : `EndEffectorPose`

## 5. ControlSixArmJoint
**Function** : Simultaneously controls all 6 joints of the robotic arm (the 6th joint controls the gripper

angle).


**Parameters** :


`runtime` : Duration of the movement (in milliseconds; Default: 1500; Range: 0 ~ 2000).


**Return Value** : `common_response`

## 6. ControlSingleArmJoint
**Function** : Sets a single robotic arm joint to a specified angle.


**Parameters** :


`arm_joint_id` : Joint ID (1-6; corresponds to robotic arm joints 1-6, where Joint 6 is the

gripper).


`runtime` : Motion duration (milliseconds; default: 1500, range: 0 ~ 2000)


**Return Value** : `common_response`

## 7. Place
**Function** : Places an object at the specified coordinates


**Parameters** :


`place_x` : X-coordinate (meters)

`place_y` : Y-coordinate (meters)

`place_z` : Z-coordinate (meters)

**Return Value:** common_response

## 8. Pick
**Function** : Grabs an object.


**Parameters** :


**Return Value** : `common_response`

## 9. AdjustCameraView
**Function** : Adjusts the camera view (pitch and yaw angles).


**Parameters** :


size: 5–10 degrees; default: 0).

`yaw` : Yaw angle adjustment (degrees; positive = right, negative = left; recommended step

size: 5–10 degrees; default: 0).


Returns `common_response` upon failure.

## 10. SeeWhat
**Function** : Captures an image from the camera and returns the path where the image is saved.


**Parameters** : None.


Returns `common_response` upon failure.

## 11. InitArmPose
**Function** : Restores the robotic arm to its preset initial pose.


**Parameters** : None.


**Return Value** : `common_response`

## 12. GetBbox
**Function** : Detects and returns the bounding box coordinates of a target object based on a

description.


**Parameters** :


Returns `BoxLocalization(bbox=bounding_box,`

`verify_image=verification_image_path)` upon success.

Returns `common_response` upon failure.


## 13. GetPlacePoint
**Function** : Retrieves the coordinates for a placement point and checks whether it lies within the

robotic arm's reachable workspace.


**Parameters** :


Returns upon success: `PlacePoint(info=info, target_point=target_point,`

```
   place_verify_image=place_verify_image_path)
```

Returns `common_response` upon failure.

## 14. AdjustChassisFitArmRange
**Function** : Quickly adjust the mobile chassis so that the target point falls within the robotic arm's

workspace.


**Parameters** :


**Return Value** : `common_response`

## 15. RecordMapLocation
**Function** : Save the current location to the map mapping file.


**Parameters** :


**Return Value** : `common_response`

## 16. GetMapMapping
**Function** : Retrieve the mapping relationship between all location names and their corresponding

symbols.


**Parameters** : None


**Return Value** : `common_response` or `str`


Returns the mapping relationship string upon success.

Returns `common_response` upon failure.


## 17. Navigation
**Function** : Navigate to a specified location using its target point symbol.


**Parameters** :


**Return Value** : `common_response`

## 18. GetWasteRecognitionResults
**Function** : Retrieve waste recognition results from the YOLO model.


**Parameters** : None


**Return Value** : `waste_recognition_result` or `common_response`


Returns the waste recognition results upon success.

Returns `common_response` upon failure.

## 19. GraspWaste
**Function** : Grasp a waste object.


**Parameters** :


**Return Value** : `common_response`

## 20. PlaceWaste
**Function** : Place a waste object.


**Parameters** : None


**Return Value** : `common_response`

## 21. TTS
**Function** : Robot Text-to-Speech (TTS) synthesis.


**Parameters** :


**Return Value** : `common_response`


## 22. Rotate
**Function** : Rotate in place by a specified angle.


**Parameters** :


**Return Value** : `common_response`

## 23. TargetTrack
**Function** : Visually track a target object


**Parameters** :


Integer: Serves as the x1 coordinate of the target tracking bounding box


**Return Value** : `common_response`

## 24. GetTargetDist
**Function** : Calculate the distance between the target and the robot chassis based on an object

description


**Parameters** :


field of view (String)


**Return Value** : `common_response`

## 25. GraspArUcoTarget
**Function** : Grasp an AprilTag target with a specified ID


**Parameters** :


**Return Value** : `common_response`

## 26. GetAprilTagIDs
**Function** : Retrieve the IDs of AprilTags currently within the field of view


**Parameters** : None


**Return Value** : `common_response`


## 27. FollowLine
**Function** : Drive along a colored line on the ground


**Parameters** :


(String)


**Return Value** : `common_response`

**Function Categories**

**Chassis Control**


MoveWithSpeed

Move

Rotate

AdjustChassisFitArmRange

Navigation


**Robotic Arm Control**


GetCurrentArmJointAngles

GetEndEffectorPose

ControlSixArmJoint

ControlSingleArmJoint

InitArmPose


**Grasping Operations**


Pick

Place

GraspWaste

PlaceWaste


**Vision Functions**


AdjustCameraView

SeeWhat

GetBbox

GetPlacePoint

TargetTrack

GetWasteRecognitionResults

GetTargetDist

GetAprilTagIDs

GraspArUcoTarget

FollowLine


**Mapping & Navigation**


RecordMapLocation

GetMapMapping

Navigation


**Speech Synthesis**


TTS
