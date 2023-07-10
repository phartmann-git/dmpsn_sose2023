![grafik](https://github.com/phartmann-git/dmpsn_sose2023/assets/83116336/d85e188a-8e10-4d3e-a6b9-ca110c7d94bf)![grafik](https://github.com/phartmann-git/dmpsn_sose2023/assets/83116336/2a359e3b-344a-4ca0-81a1-c9fcf055c0f4)![grafik](https://github.com/phartmann-git/dmpsn_sose2023/assets/83116336/6655aa71-e4f4-44a9-9aa9-5fd3899b32d5)# dmpsn_sose2023
Sign Language Recognition for learning GSL - [Designing Media for People with Special Needs]

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
