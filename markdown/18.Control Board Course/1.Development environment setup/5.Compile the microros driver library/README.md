# Compile the microros driver library
Compile the microros driver library

1. Install the cross-compiler

2. Get the STM32-microros library file

3. Modify parameters

4. Add environment variables

5. Start compiling

6. Solve the include problem

7. The final file

8. Import STM32CUBEIDE project


**Note: You must use Ubuntu to compile the microros driver library. Ubuntu 22.04 is**

**recommended.**

## 1. Install the cross-compiler
Open the download address and download the Linux version of the cross-compiler.


![](5.Compile-the-microros-driver-library.pdf-0-1.jpeg)

After decompression, put the file in the following path


And add the executable file path to the .bashrc environment variable in the user directory.


## 2. Get the STM32-microros library file
Download and compile the microros setup tool


![](5.Compile-the-microros-driver-library.pdf-1-0.jpeg)


Use the microros setup tool to generate the STM32-microros library file.


![](5.Compile-the-microros-driver-library.pdf-1-2.jpeg)

Check the workspace. We should now have five folders, among which the firmware folder

## 3. Modify parameters
Open the toolchain.cmake file


Copy the following content into

```
 set(CMAKE_SYSTEM_NAME Generic)

 set(CMAKE_CROSSCOMPILING 1)

 set(CMAKE_TRY_COMPILE_TARGET_TYPE STATIC_LIBRARY)

 # SET HERE THE PATH TO YOUR C99 AND C++ COMPILERS

 # Add the compiler path here

 set(PIX /opt/gcc-arm-none-eabi/bin)

 set(CMAKE_C_COMPILER ${PIX}/arm-none-eabi-gcc)

 set(CMAKE_CXX_COMPILER ${PIX}/arm-none-eabi-g++)

 set(CMAKE_C_COMPILER_WORKS 1 CACHE INTERNAL "")

 set(CMAKE_CXX_COMPILER_WORKS 1 CACHE INTERNAL "")

 # SET HERE YOUR BUILDING FLAGS

 set(FLAGS "-O2 -ffunction-sections -fdata-sections -fno-exceptions -mcpu=cortex
 m7 -mfpu=fpv5-d16 -mfloat-abi=hard -nostdlib -mthumb --param max-inline-insns
 single=500 -D'RCUTILS_LOG_MIN_SEVERITY=RCUTILS_LOG_MIN_SEVERITY_NONE'" CACHE

 STRING "" FORCE)

 # -mcpu=cortex-m7 indicates the microcontroller architecture

 # -mfpu=fpv5-d16 -mfloat-abi=hard indicates support for hardware floating-point

 compilation

```

```
 set(CMAKE_C_FLAGS_INIT "-std=c11 ${FLAGS} -DCLOCK_MONOTONIC=0
 D'__attribute__(x)='" CACHE STRING "" FORCE)

 set(CMAKE_CXX_FLAGS_INIT "-std=c++11 ${FLAGS} -fno-rtti -DCLOCK_MONOTONIC=0
 D'__attribute__(x)='" CACHE STRING "" FORCE)

 set(__BIG_ENDIAN__ 0)

```

Save and exit.


Open the colcon.meta file


Copy the following content into

```
 {

 "names": {

 "tracetools": {

 "cmake-args": [

 "-DTRACETOOLS_DISABLED=ON",

 "-DTRACETOOLS_STATUS_CHECKING_TOOL=OFF"

 ]

 },

 "rosidl_typesupport": {

 "cmake-args": [

 "-DROSIDL_TYPESUPPORT_SINGLE_TYPESUPPORT=ON"

 ]

 },

 "rcl": {

 "cmake-args": [

 "-DBUILD_TESTING=OFF",

 "-DRCL_COMMAND_LINE_ENABLED=OFF",

 "-DRCL_LOGGING_ENABLED=OFF"

 ]

 },

 "rcutils": {

 "cmake-args": [

 "-DENABLE_TESTING=OFF",

 "-DRCUTILS_NO_FILESYSTEM=ON",

 "-DRCUTILS_NO_THREAD_SUPPORT=ON",

 "-DRCUTILS_NO_64_ATOMIC=ON",

 "-DRCUTILS_AVOID_DYNAMIC_ALLOCATION=ON"

 ]

 },

 "microxrcedds_client": {

 "cmake-args": [

 "-DUCLIENT_PIC=OFF",

 "-DUCLIENT_PROFILE_UDP=OFF",

 "-DUCLIENT_PROFILE_TCP=OFF",

 "-DUCLIENT_PROFILE_DISCOVERY=OFF",

 "-DUCLIENT_PROFILE_SERIAL=OFF",

 "-UCLIENT_PROFILE_STREAM_FRAMING=ON",

 "-DUCLIENT_PROFILE_CUSTOM_TRANSPORT=ON",

 "-DUCLIENT_PROFILE_SHARED_MEMORY=ON",

 "-DUCLIENT_SHARED_MEMORY_MAX_ENTITIES=20"

 ]

 },

```

```
 "rmw_microxrcedds": {

 "cmake-args": [

 "-DRMW_UXRCE_MAX_NODES=1",

 "-DRMW_UXRCE_MAX_PUBLISHERS=10",

 "-DRMW_UXRCE_MAX_SUBSCRIPTIONS=10",

 "-DRMW_UXRCE_MAX_SERVICES=1",

 "-DRMW_UXRCE_MAX_CLIENTS=1",

 "-DRMW_UXRCE_MAX_HISTORY=10",

 "-DRMW_UXRCE_TRANSPORT=custom"

 ]

 }

 }

 }

```

"-DRMW_UXRCE_MAX_NODES=1", #maximum number of nodes;


"-DRMW_UXRCE_MAX_PUBLISHERS=10", #maximum number of publisher;


"-DRMW_UXRCE_MAX_SUBSCRIPTIONS=10", #maximum number of subscribers;


"-DRMW_UXRCE_MAX_SERVICES=1", #maximum number of servers;


"-DRMW_UXRCE_MAX_CLIENTS=1", #maximum number of clients;


"-DRMW_UXRCE_MAX_HISTORY=10", #history;


"-DRMW_UXRCE_TRANSPORT=custom" #custom transport interface


Save and exit.

## 4. Add environment variables
## 5. Start compiling
**Note: Since the compilation process requires downloading many files, and most file servers**

**are located abroad, if there is a network anomaly, please solve the network download**

**problem yourself.**


View the generated static library and header files


![](5.Compile-the-microros-driver-library.pdf-3-1.jpeg)


## 6. Solve the include problem
Since the generated include folder path is too long, you need to use a script to fix it.


Create a new fix_include.sh script in the firmware folder


Copy the following content into


![](5.Compile-the-microros-driver-library.pdf-4-1.jpeg)


Save and exit.


Run the following command to fix the include folder problem.


## 7. The final file
![](5.Compile-the-microros-driver-library.pdf-4-3.jpeg)


![](5.Compile-the-microros-driver-library.pdf-5-0.jpeg)
## 8. Import STM32CUBEIDE project
Create a new Microros folder in the project, and then copy the include and libmicroros folders

generated by the previous step into Microros.


Right-click to open the project properties, then click [Settings]->[MCU/MPU GCC Compiler]->

[include paths] to add the microros include directory path, and then click [Apply] to take effect.


![](5.Compile-the-microros-driver-library.pdf-6-0.jpeg)

Add the microros folder as the project source code path.


Import the microros library path


![](5.Compile-the-microros-driver-library.pdf-6-1.jpeg)

![](5.Compile-the-microros-driver-library.pdf-6-2.jpeg)
Link the microros library file to the project. Make sure the name matches the libmicroros.a static

library file name (excluding the prefix and suffix "microros").


![](5.Compile-the-microros-driver-library.pdf-7-0.jpeg)
