# Sign Language Recognition for learning GSL - [Designing Media for People with Special Needs]
This repository was used in the university course "Designing Media for People with Special Needs" short DMPSN as part of the Media Computer Science B.Sc. of the University of Applied Sciences Bremen. It serves as a code dump for presentation in the course and for saving it for the future. Main objective of this group project was to create a Sign Language Recognition which can later be used in a GSL learning app.
The content of this repository is split into 4 steps and those can be described as following:

## raw data collection
+ Collecting 24 characters, 100 frames each
+ Only non-movement letters (a-y, except j)
+ Saved as jpegs into a directory structure

## building dataset
+ Iterating through our directory structure
+ Using mediapipe to detect hand and landmarks
+ Extracting hand landmark coordinates from images
+ Only [x,y] of every landmark
+ Dumping the data into a pickle

## training the model
+ Loading dataset with 2400 samples
+ Splitting samples into training and testing data (80/20)
+ Using Random Forest technique for training
+ Accuracy score of 99.78%
+ Exporting model as independent file

## realtime testing of the model
+ Loading model
+ Getting video input from webcam
+ Detecting and analyzing hand / hand landmarks
+ Using enumerated coordinates of landmarks to predict with help of the model
+ Comparing predicted char to asked char
+ drawing prediction to hand

### webcam issue for macOS
It seems there's an error when starting video.py on macOS. This could be due to lack of permission by the terminal to start the webcam service. We haven't found a workaround for the problem so far. If you were able to fix this, please let us know on how you done that. We will share a fix to this problem as soon as we know one.
