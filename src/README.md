# Satellite receiver
Example raspberry pi ip: 10.42.0.101

## Connect to RotCtl API
The satellite receiver is controlled by rotctl. \
Run in terminal to connect to service:
```
rotctl -m 2 -r 10.42.0.101:4533
```

## Start RotCtl service
Start RotCtl service and set up virtual python environment (if needed).
```
python3 -m venv ./venv      # create venv (optional)
source ./venv/bin/activate
python3 -m pip install -r requirements.txt   # install dependencies (optional)
cd satelliteReceiver/src/
./main.py     # start controller
deactivate
```

You may need to enable I2C once in the
[raspberry pi config](https://www.raspberrypi-spy.co.uk/2014/11/enabling-the-i2c-interface-on-the-raspberry-pi).


## Connect to the pi manually
Connect ethernet adapter and raspberry first. \
Run in terminal:
```
$ ifconfig  # copy inet: (usually 10.42.0.1)
$ nmap -n -sP 10.42.0.255/24  # scans the network
```
Copy the ip address from the pi to connect to it via ssh.

Access pi via explorer:
```
nfs://10.42.0.101/home/pi/satcom/customRotatorController
```

## Headless raspberry pi setup
- pc client fstab example (static ip):
  ```  
  10.42.0.101:/home/pi/satcom/customRotatorController /home/conrad/Documents/piGitMnt nfs defaults 0 0
  ```
- [ssh](https://linuxize.com/post/how-to-enable-ssh-on-raspberry-pi/)
- [wifi](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md)
- laptop ethernet setup:
    - [static ip](https://www.circuitbasics.com/how-to-connect-to-a-raspberry-pi-directly-with-an-ethernet-cable/)
    - [dynamic ip](https://stackoverflow.com/questions/16040128/hook-up-raspberry-pi-via-ethernet-to-laptop-without-router)
- [nfs workflow](https://pimylifeup.com/raspberry-pi-nfs/)


## Used hardware
- [Power over ethernet hat](https://www.amazon.de/dp/B091YZ2QSM)
- [Motor 10RPM](https://www.banggood.com/Machifit-JGY-370-DC-12V-103090150RPM-Motor-Reduction-Gear-Turbine-Worm-Self-locking-Encoder-Signal-Feedback-Motor-p-1504101.html)
- [Magnetic encoder](https://www.amazon.de/dp/B08K2Q96V1/)
  
## Sources
- [KiCad pi Hat template](https://github.com/xesscorp/RPi_Hat_Template)
