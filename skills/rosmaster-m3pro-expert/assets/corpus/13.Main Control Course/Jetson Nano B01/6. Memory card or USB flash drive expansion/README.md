# microSD card/USB drive expansion

## Capacity Expansion Tutorial

### 1. Problem

After writing an image to a microSD card or USB drive that is larger than the image size, some free space may remain unallocated. When that happens, the system can report insufficient storage or fail to run larger projects.

Note: This tutorial is only for users who write the image themselves. If the microSD card or USB drive already contains the factory image, you can skip this tutorial.

### 2. Solution

Install the capacity expansion software and use it to expand capacity.

```bash
sudo apt install gparted
```

![Picture: page 0: picture 8](_page_0_Picture_8.jpeg)

Right click [/dev/mmcblk0p1] -> Resize/Move

![Figure: page 1: figure 1](_page_1_Figure_1.jpeg)

Drag the right box to the top until the gray area turns completely white -> Resize

![Figure: page 1: figure 3](_page_1_Figure_3.jpeg)

Click the check mark at the bottom of the function bar -> Apply

![Figure: page 2: figure 1](_page_2_Figure_1.jpeg)

Expansion completed!

![Figure: page 2: figure 3](_page_2_Figure_3.jpeg)

Use the command to query and verify in the terminal

```
df -h
```

Verify that the expansion is successful. The 32G card expansion information is as follows

![Figure: page 3: figure 0](_page_3_Figure_0.jpeg)
