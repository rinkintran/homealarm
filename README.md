# Home Alarm System for the Raspberry Pi #

### What is this repository for? ###

This code is meant to run on the Raspberry Pi to recognize people who are close by. It detects movement, captures the picture, passes it through a trained face recognizer, and verifies the face. If not recognized, it will alert the owner of the device via email. This repository is built as a computer engineering senior project.

### How do I get set up? ###

* Summary of set up
   1. Set up the RaspberryPi with the OS of your choice. I chose NOOBS. Make sure you have a 32GB MicroSD or larger since OpenCV and its extra libraries take up a lot of space.
   2. Install and enable the PiCamera
   3. Install all necessary libraries as listed below under Dependencies.
* Configuration

* Dependencies  
  * OpenCV and OpenCV-contrib
  * tensorflow-on-raspberry-pi  
  * python-picamera  

### How do I use this project? ###
1. Collect and clean data to train the face recognizer
2. Train the face recognizer
3. Run the motion detection script


Lincoln Tran  
lincoln.tran@gmail.com  
ltran28@calpoly.edu  
