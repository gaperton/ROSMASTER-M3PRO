# Jetson Nano B01 Swap space increases
![](11.-Jetson-Nano-Swap-space-increased.pdf-0-0.jpeg)


Add swapfile file size customization


sudo fallocate -l 3G /var/swapfile


Configure permissions for this file


sudo chmod 600 /var/swapfile


Establish Exchange Partition


sudo mkswap /var/swapfile


Enable swap partitioning


sudo swapon /var/swapfile


Set to automatically enable swapfile


sudo bash -c 'echo "/var/swapfile swap swap defaults 0 0" >> /etc/fstab'


View the effect and open the terminal input


![](11.-Jetson-Nano-Swap-space-increased.pdf-0-1.jpeg)


![](11.-Jetson-Nano-Swap-space-increased.pdf-1-0.jpeg)

Swap has become 6g.
