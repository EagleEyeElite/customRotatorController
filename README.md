# Satellite receiver
Project: custom rotor design for portable ground station

## headless raspberry pi setup:
- [ssh](https://linuxize.com/post/how-to-enable-ssh-on-raspberry-pi/)
- [wifi](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md)
- laptop ethernet setup:
    - [static ip](https://www.circuitbasics.com/how-to-connect-to-a-raspberry-pi-directly-with-an-ethernet-cable/)
    - [dynamic ip](https://stackoverflow.com/questions/16040128/hook-up-raspberry-pi-via-ethernet-to-laptop-without-router)
- [nfs workflow](https://pimylifeup.com/raspberry-pi-nfs/)
- pc client fstab example (static ip):
    ```  
    10.42.101:/home/pi/satcom/customRotatorController /home/conrad/Documents/piGitMnt nfs defaults 0 0
    ```
current static ip: 10.42.0.101

## connect manually to the pi (backup)
connect ethernet adapter and raspberry first. \
Run on laptop:
```
$ ifconfig  # copy inet: (usually 10.42.0.1)
$ nmap -n -sP 10.42.0.255/24  # scans the network
```
get ip address from Pi for ssh

access pi via explorer:
```
nfs://10.42.101/home/pi/satcom/customRotatorController
```

## venv workflow:
```
python3 -m venv ./venv      # create venv (optional)
source ./venv/bin/activate
python3 -m pip install -r requirements.txt   # install dependencies (optional)
deactivate
```

## used hardware:
- [Motor 10RPM](https://www.banggood.com/Machifit-JGY-370-DC-12V-103090150RPM-Motor-Reduction-Gear-Turbine-Worm-Self-locking-Encoder-Signal-Feedback-Motor-p-1504101.html)
- [pi Hat git template](https://github.com/xesscorp/RPi_Hat_Template)

## sources:
- [Encoder](https://projects.raspberrypi.org/en/projects/robotPID/2)
- [periodic tasks](https://medium.com/greedygame-engineering/an-elegant-way-to-run-periodic-tasks-in-python-61b7c477b679)
- [hardware Encoder](https://www.youtube.com/watch?v=41ogu0UlwCc)
- [hardware Encoder](https://www.allaboutcircuits.com/industry-articles/designing-quadrature-encoder-counter-with-spi-bus/)

## extras
Ticks vs Angle: \
Motor: 11 pulses per rotation, 2 Channels, 1 Pulse = two Edges \
1 Motor rotation == 44 Edges ( 1 Edge == 1 software ticks) \
Gear ratio: 600 -> 1 Shaft rotation == 44*600 == 264000 software ticks \
1° == 73,3 ticks -> hardware rotary encoder?
