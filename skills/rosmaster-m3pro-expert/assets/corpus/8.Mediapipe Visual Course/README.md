# MediaPipe Visual Course

This section covers camera-based visual interaction demos built with MediaPipe and related vision libraries. It starts with landmark detection for hands, pose, face mesh, and holistic body tracking, then moves into visual effects, 3D object recognition, air drawing, finger-based image control, palm positioning, trajectory recognition, and robotic-arm gesture control.

Use this section when you need to understand how camera image topics are converted into visual landmarks, gestures, drawing paths, or robotic-arm commands.

## [8.1 Hand Detection](./1.Hand%20detection/README.md)

Shows how to capture color images and use MediaPipe Hands to detect hand landmarks. The lesson displays the original camera image beside a landmark-only view and explains the ROS image subscriber, `CvBridge` conversion, MediaPipe hand detector, and image-stitching display function.

## [8.2 Posture Detection](./2.Posture%20detection/README.md)

Uses MediaPipe Pose to detect human body landmarks from the camera stream. The lesson starts the camera and pose detector, draws the detected body skeleton, and explains how pose landmarks are processed and rendered.

## [8.3 Holistic Detection](./3.Overall%20detection/README.md)

Uses MediaPipe Holistic to detect face, hand, and body landmarks in one pipeline. The lesson shows how the holistic detector combines face mesh, hand landmarks, and pose landmarks and displays them beside the original camera image.

## [8.4 Facial Landmark Detection](./4.Facial%20Landmark%20Detection/README.md)

Uses MediaPipe Face Mesh to detect and draw facial landmarks. The lesson covers camera startup, face-mesh processing, landmark rendering, and the shared image-stitching helper used by earlier MediaPipe demos.

## [8.5 Face Detection](./5.Face%20detection/README.md)

Uses MediaPipe Face Detection to locate faces in the camera image. The program draws stylized bounding boxes around detected faces and overlays confidence scores so users can inspect detection quality.

## [8.6 Face Special Effects](./6.Face%20special%20effects/README.md)

Uses dlib facial landmarks to apply simple effects to the eyes, mouth, and eyebrows. The lesson explains the 68-point facial landmark layout, the dlib face detector and predictor, and the helper functions that collect facial regions and fill them with effect colors.

## [8.7 3D Object Recognition](./7.3D%20object%20recognition/README.md)

Uses MediaPipe Objectron to recognize selected 3D objects from the camera image. The demo supports shoe, chair, cup, and camera categories, lets the user switch targets with `F`, and draws the detected 3D box and coordinate axis.

## [8.8 Air-Drawing Brush](./8.Brush/README.md)

Turns finger movement into a virtual drawing brush. The lesson uses MediaPipe hand landmarks to switch between color-selection mode and drawing mode, supports red, green, blue, yellow, and black eraser colors, and explains the canvas compositing logic.

## [8.9 Finger Control](./9.Finger%20control/README.md)

Uses the angle between the thumb, wrist, and index fingertip to adjust image-processing effects. The lesson shows how to switch effects with `F` and control thresholding, blur, hue, or contrast intensity by opening and closing the thumb-index angle.

## [8.10 Palm Target Positioning](./10.Palm%20target%20positioning/README.md)

Detects a hand and outputs the palm center coordinates. This provides a basic target-positioning pattern that can be reused for chassis or robotic-arm tracking behaviors.

## [8.11 Fingertip Trajectory Recognition](./11.Fingertip%20trajectory%20recognition/README.md)

Records a fingertip path and classifies the drawn trajectory. The lesson uses an open-palm gesture to reset or finish, a one-finger gesture to draw, and recognizes closed shapes such as triangle, rectangle, circle, and five-pointed star.

## [8.12 Fingertip Gesture Control of Robotic Arm](./12.Fingertip%20gesture%20control%20robotic%20arm/README.md)

Extends fingertip trajectory recognition by mapping recognized shapes to robotic-arm movements. The program records a drawn shape, recognizes it, then starts an arm-control thread that runs the corresponding action.

## [8.13 Gesture Grabbing and Releasing Objects](./13.Gesture%20grabbing%20and%20releasing%20objects/README.md)

Uses MediaPipe gesture recognition to trigger robotic-arm grasp and release actions. A `Yes` gesture moves the arm to grasp an object, while an `OK` gesture places the object at a preset location.

## [8.14 Finger Control of Robotic Arm](./14.Finger%20control%20robotic%20arm/README.md)

Controls the robotic-arm gripper with the angle between the thumb and index finger. The lesson maps the detected finger angle to servo No. 6 so opening and closing the hand gesture changes the gripper opening.

## [8.15 MediaPipe Gesture Control of Arm Action Group](./15.Medipipe%20gesture%20control%20robotic%20arm%20action%20group/README.md)

Maps recognized gestures to predefined robotic-arm action groups. The lesson supports gestures such as `Yes`, `OK`, `Thumb_down`, one finger, Rock, and five fingers, and triggers each action group when the spacebar is pressed.
