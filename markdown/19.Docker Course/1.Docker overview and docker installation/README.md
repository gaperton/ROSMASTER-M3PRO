# 1、Docker overview and docker
# installation
_**At present, ROS2's courses are all placed in Docker containers, and customers can experience**_

_**learning to use containerized development methods.**_

## 1、Docker overview and docker installation
### 1.1、Docker overview

#### 1.1.1、why docker appears

#### 1.1.2、Docker's core idea

#### 1.1.3、Compare virtual machines to Docker

#### 1.1.4、docker architecture

#### 1.1.5、Docker core objects

#### 1.1.6、images, containers, repositories

#### 1.1.7、Docker operation mechanism

### 1.2、docker installation


Docker Chinese website: [https://www.docker-cn.com](https://www.docker-cn.com/)


Docker Hub (repository) official website: [https://hub.docker.com](https://hub.docker.com/)


The operating environment and software and hardware reference configurations are as follows:


REFERENCE MODEL: ROSMASTER X3


Robot hardware configuration: Arm series main control, Silan A1 lidar, AstraPro Plus depth

camera


Robot system: Ubuntu (version not required) + docker (version 20.10.21 and above)


PC Virtual Machine: Ubuntu (20.04) + ROS2 (Foxy)


Usage scenario: Use on a relatively clean 2D plane
### 1.1、Docker overview
Docker is an application container engine project, developed based on the Go language and open

source.

#### 1.1.1、why docker appears
Let's start with a few scenarios:


1. O&M deploys the project you developed to the server, telling you that there is a problem and

cannot be started. You ran around locally and found that there was no problem...


2. The project to be launched is unavailable due to the update of some software versions...


3. There are a lot of environmental content involved in the project, various middleware, various

configurations, and the deployment of multiple servers...


These problems can actually be summed up in relation to the environment.

To avoid various problems caused by different environments, it is best to deploy the project

together with the various environments required by the project.

For example, the project involves environments such as REDIS, MYSQL, JDK, ES, etc., and the entire

environment is brought with you when deploying the JAR package. So the question is, how can you

bring the project with the environment?


Docker is here to solve this problem!

#### 1.1.2、Docker's core idea
This is the logo of Docker, a whale full of containers, on the back of the whale, the containers are

isolated from each other, which is the core idea of Docker.

For example, if there were multiple applications running on the same server before, there may be

port occupation conflicts of software, but now they can run alone after isolation. In addition,

Docker can maximize the power of the server.

#### 1.1.3、Compare virtual machines to Docker
The docker daemon can communicate directly with the main operating system to allocate

resources to individual docker containers; It can also isolate containers from the main

operating system and isolate individual containers from each other. Virtual machines take

minutes to start, while docker containers can start in milliseconds. Since there is no bloated

from the operating system, Docker can save a lot of disk space as well as other system

resources.


![](1、Docker-overview-and-docker-installation.pdf-1-0.jpeg)

![](1、Docker-overview-and-docker-installation.pdf-1-1.jpeg)
Virtual machines are better at completely isolating the entire operating environment. For

example, cloud service providers often use virtual machine technology to isolate different

users. Docker is often used to isolate different applications, such as front-end, back-end, and

database.


Docker containers are more resource-efficient and faster (start, shut down, create, delete)

than virtual machines

#### 1.1.4、docker architecture
Docker uses a client-server architecture. The Docker client communicates with the Docker

daemon, which is responsible for building, running, and distributing the Docker container. The

Docker client and daemon can run on the same system, or you can connect a Docker client to a

remote Docker daemon. The docker client and daemon communicate using REST APIs over UNIX

sockets or network interfaces. Another Docker client is Docker Compose, which lets you work with

applications that consist of a set of containers.


docker client is a docker command that is used directly after installing docker.


Docker host is our docker host (i.e. the operating system on which docker is installed)


Docker Daemon is Docker's background daemon that listens for and processes Docker client

commands and manages Docker objects such as images, containers, networks, and volumes.


registry is a remote repository where docker pulls images, providing a large number of

images for download, and saving them in images (local image repository) after downloading.


Images is a local image repository of docker, and image files can be viewed through docker

images.


![](1、Docker-overview-and-docker-installation.pdf-2-0.jpeg)
#### 1.1.5、Docker core objects
#### 1.1.6、images, containers, repositories
Image:


![](1、Docker-overview-and-docker-installation.pdf-3-0.jpeg)

![](1、Docker-overview-and-docker-installation.pdf-3-1.jpeg)


Container:


![](1、Docker-overview-and-docker-installation.pdf-3-2.jpeg)


Repository:


![](1、Docker-overview-and-docker-installation.pdf-3-3.jpeg)


You need to correctly understand the concepts of warehousing/image/container:


Docker itself is a container runtime carrier, or management engine. We package the

application and configuration dependencies to form a shippable runtime environment, and

this packaged runtime environment is like an image image file. Only this image file can

generate a docker container. An image file can be thought of as a template for a container.

Docker generates an instance of the container from the image file. The same image file

allows you to generate multiple container instances running at the same time.


The container instance generated by the image file is itself a file, called an image file.


A container runs a service, and when we need it, we can create a corresponding running

instance through the docker client, which is our container.


As for the repository, it is a place where a bunch of images are placed, we can publish the

images to the repository, and pull them from the repository when needed.

#### 1.1.7、Docker operation mechanism
Docker pull execution process:


1. The client sends instructions to Docker Daemon


2. Docker Daemon first check whether there are relevant images in the local images


3. If there is no relevant image locally, request the mirror server to download the remote mirror

to the local computer


docker run execution process:


1. Check whether the specified image exists locally and download it from the public repository


2. Create and start a container from the image


3. Assign a file system (lite Linux system) and mount a read-write layer outside the read-only

image layer


4. Bridge a virtual interface from the bridge interface configured by the host to the container


5. Configure an IP address from the address pool to the container


6. Execute the application specified by the user
### 1.2、docker installation
1. Official website installation reference manual: https://docs.docker.com/engine/install/ubunt

u/


2. You can use the following commands to install with one click:


3. Check the docker version


![](1、Docker-overview-and-docker-installation.pdf-5-0.jpeg)

4. Test the command


The following output indicates that the Docker installation was successful


![](1、Docker-overview-and-docker-installation.pdf-6-0.jpeg)
