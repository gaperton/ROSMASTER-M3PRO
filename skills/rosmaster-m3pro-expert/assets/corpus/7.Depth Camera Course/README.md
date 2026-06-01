# Depth Camera Course

This section covers the ROSMASTER-M3PRO depth-camera stack and the vision tasks built on top of it. It starts with the Orbbec Dabai DCW2 camera driver and ROS image topics, then moves through depth visualization, distance and volume measurement, gesture recognition, edge detection, YOLOv8 object detection, and TensorRT-based object tracking.

Use this section when you need to work with RGB, depth, infrared, or point-cloud data from the camera, or when you want to build robot behaviors that depend on depth perception, hand gestures, object detection, and visual target tracking.

## [7.1 Orbbec Dabai DCW2 Camera Overview](./1.Dabai_DCW2%20camera%20introduction/README.md)

Introduces the Dabai DCW2/DW2 depth camera, its structured-light depth sensing, RGB camera, operating range, and hardware features. The lesson shows how to start the `orbbec_camera` driver, inspect the `/camera/camera` node, view color, depth, and infrared image topics, and display registered or unregistered point clouds in RViz.

## [7.2 Depth Pseudocolor Visualization](./2.Depth%20pseudo-color%20image/README.md)

Shows how to subscribe to `/camera/depth/image_raw` and convert grayscale depth data into a pseudocolor image with OpenCV. The lesson covers starting the camera, running `GetDepthColor`, converting ROS image messages with `CvBridge`, scaling depth values, and applying OpenCV color maps such as `COLORMAP_JET`.

## [7.3 Depth-Based Distance Measurement](./3.Depth%20camera%20distance%20measurement/README.md)

Explains how to measure distance from the depth camera by selecting a point in the image. The program displays a pseudocolor depth image, lets the user click a valid image point, reads the corresponding depth value from the converted depth array, and prints the measured distance in millimeters on the image.

## [7.4 Depth-Based Object Volume Measurement](./4.Wood%20block%20volume%20measurement/README.md)

Combines depth images, RGB images, robotic-arm pose data, and coordinate-frame transformations to estimate wooden-block volume. The lesson starts the camera and arm kinematics program, runs `estimate_volume`, uses synchronized RGB/depth data and arm offset calibration values, calculates object center and vertex coordinates in the world frame, and compares measured volume with the theoretical block volume.

## [7.5 MediaPipe Gesture Recognition](./5.Mediapipe%20gesture%20recognition/README.md)

Introduces MediaPipe Hands and runs a gesture-recognition demo using the camera color image topic. The lesson explains MediaPipe's hand landmark model, starts `mediapipe_gesture`, recognizes gestures such as `OK`, `Yes`, and `Thumb_down`, and shows how image callbacks, hand landmarks, and geometric gesture logic are used to trigger robot-arm posture behavior.

## [7.6 Depth-Based Edge Detection](./6.Edge%20detection/README.md)

Shows how depth imaging can detect an edge in front of the robot and stop chassis movement before a fall risk. The program starts from a stopped state, moves forward after the spacebar is pressed, reads depth information near the center of the image, publishes `/cmd_vel` movement or stop commands, and positions the robotic arm for downward edge observation.

## [7.7 YOLOv8 Object Detection](./7.YOLOv8%20object%20detection/README.md)

Introduces YOLOv8 object detection on Orin boards. The lesson starts the depth camera, runs the YOLOv8 detection node, publishes annotated detection images on `/detect_image`, and uses `rqt_image_view` to inspect bounding boxes, class labels, confidence values, and tracking IDs generated from the camera color stream.

## [7.8 TensorRT Object Tracking](./8.Deep%20learning%20object%20tracking/README.md)

Shows how YOLOv8 tracking is optimized with TensorRT on Orin boards for real-time object following. The lesson starts the camera and LiDAR tracking launch file, runs the TensorRT tracking node, selects a target by publishing its ID to `/tracker_id`, and uses camera alignment plus LiDAR distance feedback so the robot follows the selected object while maintaining a target distance.
