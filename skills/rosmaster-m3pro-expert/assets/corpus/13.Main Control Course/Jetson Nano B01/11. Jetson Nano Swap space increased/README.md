# Jetson Nano B01 Swap space increases

Entering the following commands in sequence can increase the swap space by 3G and solve some program errors that run out of memory.

```
sudo fallocate -l 3G /var/swapfile
sudo chmod 600 /var/swapfile
sudo mkswap /var/swapfile
sudo swapon /var/swapfile
sudo bash -c 'echo "/var/swapfile swap swap defaults 0 0" >> /etc/fstab'
```

Add swapfile file size customization

sudo fallocate -l 3G /var/swapfile

Configure permissions for this file

```bash
sudo chmod 600 /var/swapfile
```

Establish Exchange Partition

sudo mkswap /var/swapfile

Enable swap partitioning

sudo swapon /var/swapfile

Set to automatically enable swapfile

sudo bash -c 'echo "/var/swapfile swap swap defaults 0 0" >> /etc/fstab'

View the effect and open the terminal input

```
jtop
```

```
   jtop MAXN|CPU 11.9%|GPU 14.2%
Model: NVIDIA Jetson Nano Developer Kit - Jetpack 4.6.3 [L4T 3
               19.2%] 825MHz 3 [||||| 30.0%] 1.3GHz 24.8%] 921MHz 4 [||| 23.0%] 1.3GHz
21 .[||
                                0.0%]
2 [||
Mem [||||||||||||| 1.2G/3.9G] FAN [
                                                    0RPM
                    0k/5.9G] Jetson Clocks: inactive
Emc RUNNING -  1.6GHz 0% NV Power[0]: MAXN
Iram [
                                             14.2%] 153MHz
Dsk [####################################
                                             31.7G/57.0G]
PID
      USER
              GPU TYPE PRI S
                                  CPU%
                                         MEM
                                                [GPU MEM]
5998
      jetson
              I
                   G
                         20
                              S
                                  4.0
                                         9.8M
                                                39.8M
7034
      ietson
              I
                  G
                         20
                              R
                                  3.5
                                         26.0M
                                                33.1M
5284
              I
                              S
                                        4.7M
     root
                  G
                         20
                                  0.0
                                                76k
      - [HW engines] -
                                 -[Sensor] -- [Temp]
  APE: 25.5MHz
                                               41.00C
                                   AO
  NVENC: [OFF] NVDEC: [OFF]
                                   CPU
                                               31.50C
  NVJPG: [OFF] SE: [OFF]
                                   GPU
                                               29.50C
                                   iwlwifi
                                               46.00C
                                                29.50C
                                   PLL
                                   thermal
                                               31.00C
```

Swap has become 6g.
