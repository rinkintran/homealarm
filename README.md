# Home Alarm System for the Raspberry Pi #

### What is this repository for? ###

This code is meant to run on the Raspberry Pi to recognize people who are close by. It detects movement, captures the picture, passes it through a trained face recognizer, and verifies the face. If not recognized, it will alert the owner of the device via email. This repository is built as a computer engineering senior project.

### How do I get set up? ###

* Summary of set up
   1. Set up the RaspberryPi with the OS of your choice. I used NOOBS to install Raspbian. Make sure you have a 32GB MicroSD or larger since OpenCV and its extra libraries take up a lot of space. [This](https://www.raspberrypi.org/documentation/installation/noobs.md) is a really good guide on how to get started on the Raspberry Pi.
   2. Install and enable the PiCamera following these [instructions](https://www.raspberrypi.org/documentation/usage/camera/python/README.md).
   3. Install OpenCV as well as the secondary repository OpenCV-contrib, since that contains the face recognition library. The compilation and installation instructions can be found [here](https://docs.opencv.org/trunk/d7/d9f/tutorial_linux_install.html). Make sure to increase the swap file size so that make can run properly. Instructions to change swap file size can be found [here](https://raspberrypi.stackexchange.com/questions/70/how-to-set-up-swap-space).

* Dependencies  
  * OpenCV and OpenCV-contrib
  * python-picamera  

### Hardware Setup ###
None of this code would work properly if the hardware was not set up properly. There isn't really a defined way to configure the camera, as long as it has a clear view of the subject. I'd recommend setting the camera at eye level or a little higher so it can get a good angle of the face. Here is what my setup looks like:
[setup] .jpg "Setup"

### How do I use this project? ###
1. Collect and clean data to train the face recognizer
  1. There are two ways to train this project.
    1. You can either collect your own pictures and copy them into the `/imagesToProcess` folder to run the `cropFaces.py` script.
  ```bash
  python3 cropFaces.py yourImage.jpg
  ```
   This will output a new file for every face found in the image. You will have to rename each image and copy it into the correct folder for that person.
   2. The other way is to just let the camera monitor normal activity in the room for a few days. Running the `/inProgress/dataCollection/collectData.py` script will record all faces that pass in front of the camera. After a few days, there should be enough images of faces to train off of. I think this method is better since these images are more accurate for comparison versus pictures taken on a different camera. Each image still need to be identified and labeled by hand.

  2. The folder of known images is called ```/knownFaces```. I left it out of the GitHub repository since it only contained pictures of our faces. Within this folder, create another folder for each person you would like to add to the database. Each person should have at least 10 good images so the model has good data to compare against. Number each image from 0 to the number of images.

  3. Run the script `train.sh` in the home directory. This will remove the existing trained data, if it exists, create a map of all the known face images, and pass it to the trainer to create a data file of known faces. Any future faces will be compared to all the data in the `faceModel.yml` file.

2. Setup email parameters
  - This process will vary per email service. I am using Gmail's SMTP server and authenticating with OAuth2. Google has a good [guide](https://github.com/google/gmail-oauth2-tools/wiki/OAuth2DotPyRunThrough) on how to authenticate using Python. Read through it and once you set up your account, add your info into a file called `userInfo.py`. It should look like this:
  ```python
  client_id = "1*******.apps.googleusercontent.com"
  client_secret = "*******"
  refresh_token = "1/S********__YpUi-C6CS"
  ```
  The stars are just to censor my private information.

3. Run the motion detection script
   - After following the steps above, everything should be setup! Now all we have to do is run the program and it will notify you by email if an unknown face is detected.
   ```bash
   python3 detectFaces.py
   ```

#### Contact Info: ####
Lincoln Tran  
lincoln.tran@gmail.com  
ltran28@calpoly.edu  
