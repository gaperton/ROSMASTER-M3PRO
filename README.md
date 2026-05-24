# ROSMASTER M3 Pro ROS2 Robot for Jetson NANO B01/Orin NX SUPER/Orin NANO SUPER/RPi 5
![](https://github.com/YahboomTechnology/ROSMASTER-M3PRO/blob/main/ROSMASTER_M3PRO.jpg)
# Introduction
ROSMASTER M3 Pro is a highly integrated embodied intelligent robot platform developed by Yahboom specifically for ROS education, scientific research experiments, and AI application teaching. It utilizes Mecanum wheels and pendulum suspension chassis for omnidirectional movement. Developed based on the ROS2 Humble system, equipped with a 6DOF robotic arm and a binocular structured light depth camera to perform tasks such as visual recognition, 3D grasping, and precise handling. With dual TOF LiDAR, it enables stable and reliable SLAM mapping and autonomous navigation, as well as LiDAR obstacle avoidance and path planning. Unlike traditional ROS robots, the ROSMASTER M3 Pro deeply integrates cutting-edge AI large-scale model technology. Built-in speech recognition and natural language understanding modules, can realize voice command control, multimodal interaction with text/image/voice, task planning and execution, and dynamic environment perception. Whether used in AI courses, robotics algorithm teaching, or university research projects, the ROSMASTER M3 Pro provides a stable, powerful, and easily scalable experimental platform, making it an ideal choice for AI and robotics education.
# Features
【Top-level Hardware Configuration】

* Raspberry Pi 5, Jetson NANO B01, Jetson ORIN NANO SUPER, Jetson ORIN NX SUPER development boards, four main control boards for choice.
* An aluminum alloy chassis, 80mm Mecanum wheels, and a rear-wheel pendulum suspension structure allow for easy navigation across diverse terrains.
* Combining a depth camera and a 6DOF robotic arm, it enables 3D grasping, precise handling, and MoveIt simulation. 4. Two TOF ranging LiDAR on the front left and rear right provide 360° scanning, enhancing mapping and navigation accuracy.
* 
【Fully Integrates Intelligent Perception and Semantic Understanding】

* Built-in speech recognition and natural language processing, combined with speakers, enable easy voice commands and question-and-answer interactions.
* Integrating multimodal interaction capabilities, including text, image, and voice, it can adjust actions in real time based on environmental changes, supporting free conversation interruptions and dynamic feedback reasoning.
* Integrating a large model and an extensible RAG knowledge system enhances task awareness and complex problem-solving capabilities.

【A full-stack robotics platform for teaching and research】

* Based on the ROS2 Humble system, compatible with a variety of robotics algorithms and AI course content.
* Integrated hardware and software, along with comprehensive documentation and teaching resources, facilitate efficient progress from introductory learning to scientific research experiments.
* From AI and SLAM to visual recognition and robot control, it's widely applicable to university teaching, scientific research experiments, and robotics competition platform development.

# More Details
[Click here](https://category.yahboom.net/products/rosmaster-m3-pro)

# Markdown Documentation

All 246 course PDFs have been converted to Markdown under [markdown/](markdown/), mirroring the original folder tree. For each `<course>/<lesson>.pdf` you'll find `markdown/<course>/<lesson>/<lesson>.md` plus the extracted figures (`.jpeg`) and a `<lesson>_meta.json` alongside. Tables, code blocks, headings, and images are preserved.

## How to regenerate

Conversion uses [marker-pdf](https://github.com/datalab-to/marker) with CUDA-accelerated PyTorch. Tested on Windows 11 + Python 3.12 + RTX 2070 (CUDA 12.8). Full batch runs in ~50 min on that GPU; CPU-only is possible but much slower.

1. **Install Python 3.10+** (3.12 recommended):
   ```powershell
   winget install Python.Python.3.12
   ```
2. **Install PyTorch with CUDA** (pick the build matching your driver from [pytorch.org](https://pytorch.org/get-started/locally/)):
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
   ```
   For CPU only: `python -m pip install torch torchvision`.
3. **Install marker and its batch dependency:**
   ```powershell
   python -m pip install marker-pdf psutil
   ```
4. **Run the conversion** from the repo root:
   ```powershell
   python markdown/convert_all.py
   ```
   The script is resumable — it skips any PDF whose target `.md` already exists and is non-empty. On first run, marker downloads its layout/OCR models (~2 GB) into the HuggingFace cache.

5. **(Windows only) Fix long-path failures.** Two PDFs in `3.AI Model - Text Version/` and `4.AI Model - Voice Version/` produce target paths over the Windows 260-char `MAX_PATH` limit. After step 4, run:
   ```powershell
   python markdown/fix_longpath.py
   ```
   This converts those two via a short temp path and writes them one folder shallower (`markdown/<course>/<lesson>.md` instead of `markdown/<course>/<lesson>/<lesson>.md`). Alternatively, enable Win32 long paths permanently:
   ```powershell
   # admin PowerShell, then reboot
   Set-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem' LongPathsEnabled 1
   ```

# Please Contact Us
If you have any problem when using our robot after checking the tutorial, please contact us.

### WhatsApp:
+86 18682378128

### Technical support email: 
support@yahboom.com
