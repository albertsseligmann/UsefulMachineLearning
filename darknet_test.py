#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 20:19:43 2020

@author: albert
"""

import cv2
import numpy as np
from darknet import darknet
import time


# Assuming file is being run from wdir='home/bla/bla/31392_project'
detectorConfigPath = "detector/cfg/yolov3-spp.cfg"
detectorWeightPath = "detector/weights/yolov3-spp_final.weights"
# detectorWeightPath = "detector/weights/yolov3-spp_31392_final.weights"
detectorMetaPath = "detector/cfg/yolo31392.data"
detectorThresh = 0.05 # Open Images weights without our own training occasionally has confidence around 0.03 on some sample boxes...

validClasses = ["Cup", "Book", "Box"]


def detectorFilterClasses(detections, validClasses): # Keep only relevant objects
    return [i for i in detections if i[0] in validClasses]

def detectorInitialise():
    print("Initialising detector")
    darknet.performDetect(
                        configPath    = detectorConfigPath, 
                        weightPath    = detectorWeightPath,
                        metaPath      = detectorMetaPath,
                        initOnly      = True)  # Only initialize globals. Don't actually run a prediction.

def detectorDetect(imageRGB, timing = False):
    ### Do detection
    prev_time = time.time() # Time
    print("Performing detection of RGB image")
    detections = darknet.performDetectAS(
        imageInRGB    = imageRGB, # MUST BE RGB
        thresh        = detectorThresh, 
        configPath    = detectorConfigPath, 
        weightPath    = detectorWeightPath,
        metaPath      = detectorMetaPath,
        showImage     = False, # Shows image using scikit - halts execution
        makeImageOnly = False, # If showImage is True, this won't actually *show* the image, but will create the array and return it.
        initOnly      = False) # Only initialize globals. Don't actually run a prediction.
    if timing:
        print("Detected in " + str((time.time()-prev_time)*1000) + " ms")
    return detections

def detectorDetectBGR(imageBGR, timing = False):
    ### Do detection
    imageRGB = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2RGB)
    prev_time = time.time() # Time
    print("Performing detection of BGR image")
    detections = darknet.performDetectAS(
        imageInRGB    = imageRGB, # MUST BE RGB
        thresh        = detectorThresh, 
        configPath    = detectorConfigPath, 
        weightPath    = detectorWeightPath,
        metaPath      = detectorMetaPath,
        showImage     = False, # Shows image using scikit - halts execution
        makeImageOnly = False, # If showImage is True, this won't actually *show* the image, but will create the array and return it.
        initOnly      = False) # Only initialize globals. Don't actually run a prediction.
    if timing:
        print("Detected in " + str((time.time()-prev_time)*1000) + " ms")
    return detections

def detectorDetectFile(filepath, timing = False):
    prev_time = time.time() # Time
    print("Performing detection of " + detectorFilePath)
    detections = darknet.performDetect(
                            imagePath     = detectorFilePath, 
                            thresh        = detectorThresh, 
                            configPath    = detectorConfigPath, 
                            weightPath    = detectorWeightPath,
                            metaPath      = detectorMetaPath,
                            showImage     = False, # Shows image using scikit - halts execution
                            makeImageOnly = False, # If showImage is True, this won't actually *show* the image, but will create the array and return it.
                            initOnly      = False) # Only initialize globals. Don't actually run a prediction.
    if timing:
        print("Detected in " + str((time.time()-prev_time)*1000) + " ms")
    return detections




### Initialise
detectorInitialise()

### Prep image
detectorFilePath = "data/course/sample_stereo_conveyor_without_occlusions/left/left_0042.png"
imBGR = cv2.imread(detectorFilePath) # BGR
imRGB = cv2.cvtColor(imBGR, cv2.COLOR_BGR2RGB)

### Do detection
# RGB image
detections1 = detectorDetect(imRGB, timing = True)
print(detections1)

# BGR image
detections2 = detectorDetectBGR(imBGR, timing = True)
print(detections2)

# File
detections3 = detectorDetectFile(detectorFilePath, timing = True)
print(detections3)

# Filter detections
detections = detectorFilterClasses(detections1, validClasses)
print(detections)

