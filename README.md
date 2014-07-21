raspicam_motionDetection
========================
This project uses the official Raspberry Pi Camera module along with the latest Raspbian Weezy image:
http://downloads.raspberrypi.org/raspbian_latest

Dont forget to activate the camera using:
```
sudo raspi-config
```
Make sure your RPi is up to date:
sudo apt-get update
sudo apt-get upgrade

Download and install the Python Dependencies
sudo apt-get install python-pip python-dev python-numpy

Download and install the picamera interface
sudo pip install picamera

Download and install OpenCV
sudo apt-get install libopencv-dev python-opencv
