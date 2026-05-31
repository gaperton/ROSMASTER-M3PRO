# Precautions for the DIY Robotic Arm

Note: When the robotic arm grips an object, you must set the gripper angle correctly. An incorrect angle may stall the servo and can burn it out.

The table below lists the recommended gripper servo angle for each object length, in 0.5 cm increments.

Use this table when setting the gripping angle to avoid stalling the servo.

![Picture: page 0: picture 4](_page_0_Picture_4.jpeg)

| Object length (cm) | Servo angle (degrees) |
|--------------------|-----------------------|
| 0                  | 180                   |
| 0.5                | 176                   |
| 1.0                | 168                   |
| 1.5                | 160                   |
| 2.0                | 152                   |
| 2.5                | 143                   |
| 3.0                | 134                   |
| 3.5                | 125                   |
| 4.0                | 115                   |
| 4.5                | 105                   |
| 5.0                | 95                    |
| 5.5                | 80                    |
| 6.0                | 57                    |
| 6.0-6.4            | 0-57                  |

For example, the provided visual-recognition cube is 3 cm long, 3 cm wide, and 3 cm high. To grip it, set the gripper servo angle to 134 degrees. Do not set the angle too large.

![Picture: page 2: picture 0](_page_2_Picture_0.jpeg)

Note: This product includes wooden blocks with four different sizes and shapes. When performing gripping operations, strictly use the block dimensions specified in the tutorial. For example, if the program is configured to grip a 3 cm cube but you place a 4 cm cube instead, servo No. 6 may be damaged.

![Picture: page 2: picture 2](_page_2_Picture_2.jpeg)
