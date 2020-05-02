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
import os


def detectorFilterClasses(detections, validClasses, aliasClasses): # Keep only relevant objects
    filtered = []
    for i in detections:
        if i[0] in aliasClasses:
            alias = aliasClasses[i[0]]
            filtered.append((alias, i[1], i[2]))
        elif i[0] in validClasses:
            filtered.append(i)
    return filtered

def detectorGetBest(detections): # Keep only relevant objects
    temp = 0
    best = []
    if len(detections) > 0 and detections is not None:
        for i in detections:
            if i[1] >= temp:
                temp = i[1]
                best = i
                print("Best: " + str(best))
        return [best]
    else:
        return best

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

def drawObject(img, text, color, x, y, w, h):
    # Function to draw bounding box on image
    # x, y is center coordinates
    thickness_box = 4
    thickness_text = 2
    
    # Define points
    x0 = int(x - w/2) # top left
    y0 = int(y - h/2)
    x1 = int(x + w/2) # bottom right
    y1 = int(y + h/2)
    
    # Draw
    cv2.rectangle(img, (x0, y0), (x1, y1), color, thickness_box)
    cv2.putText(img, text, (x0, y0 - 5), cv2.FONT_HERSHEY_PLAIN, 1, color, thickness_text)
    
    return img

# Assuming file is being run from wdir='home/bla/bla/31392_project'
detectorConfigPath = "detector/cfg/yolov3-spp_31392.cfg"
#detectorConfigPath = "detector/cfg/yolov3-spp.cfg"
detectorWeightPath = "detector/weights/yolov3-spp_31392_final.weights"
#detectorWeightPath = "detector/weights/yolov3-spp_final.weights"
detectorMetaPath = "detector/cfg/yolo31392.data"
detectorThresh = 0.10 # Open Images weights without our own training occasionally has confidence around 0.03 on some sample boxes...

validClasses = ["Cup", "Book", "Box"]
aliasClasses = {"Mug": "Cup", "Coffee cup": "Cup"}


### Initialise
print("--------------------- INITIALISING ---------------------")
detectorInitialise()

print("--------------------- TESTING ---------------------")
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
detections = detectorFilterClasses(detections1, validClasses, aliasClasses)
print(detections)

print("--------------------- DONE TESTING ---------------------")


debug = True
writeLabel = False

# Define constants
classNameID = {"Box": 269, "Book": 68, "Cup": 56,}
classIDName = {269: "Box", 68: "Book", 56: "Cup"}
classIDColor = {269: (255, 0, 0), 68: (0, 255, 0), 56: (0, 0, 255)}

path = "data/train/cup/cup00001"
path = "data/course/Stereo_conveyor_without_occlusions/left"

# Find content at path
content = sorted(os.listdir(path))
imgs = []
for string in content:
    if (string[-4:] == ".jpg") or (string[-4:] == ".png"): # Choose images
        imgs.append(string)

i = 0
while True:
    # Read image
    filename_img = imgs[i]
    path_current_img = os.path.join(path, filename_img)
    img = cv2.imread(path_current_img)
    
    # Read label
    filename_label = imgs[i][:-4] + ".txt"
    path_current_label = os.path.join(path, filename_label)
    if debug:
        print("\n" + path_current_img)
        
    # Detect anf filter
    detections_all = detectorDetectBGR(img, timing = True)
    detections_filter = detectorFilterClasses(detections_all, validClasses, aliasClasses)
    detections = detectorGetBest(detections_filter)
    if debug:
        print("All detections:")
        print(detections_all)
        print("Filtered detections:")
        print(detections_filter)
        print("Best detection:")
        print(detections)
    
    img_labels = []
    for cnt, det in enumerate(detections): # Go through each line
        try: 
            # Read label information
            
            ID = int(classNameID[det[0]]) # Class ID
            x = float(det[2][0]) # x center
            y = float(det[2][1]) # y center
            w = float(det[2][2]) # width
            h = float(det[2][3]) # height
            conf = float(det[1])
            
            # Add label information to list
            this_label = [ID, conf, x, y, w, h]
            img_labels.append(this_label)
            
        except ValueError:
            print("Something went wrong with the label")
    
#    ID = int(detections[0]) # Class ID
#    x = float(detections[1]) # x center
#    y = float(detections[2]) # y center
#    w = float(detections[3]) # width
#    h = float(detections[4]) # height
    
    # Get image dimensions
    img_dim = img.shape
    img_h = img_dim[0]
    img_w = img_dim[1]
    img_c = img_dim[2]
    
    # Draw bounding box
    for bbox in img_labels:
        bbox_name = classIDName[bbox[0]] # Get name and color form ID
        bbox_color = classIDColor[bbox[0]]
        bbox_conf = bbox[1]
        bbox_x = bbox[2] # Absolute
        bbox_y = bbox[3] 
        bbox_w = bbox[4] 
        bbox_h = bbox[5]
#        bbox_x = bbox[2] * img_w # Go from relative to absolute
#        bbox_y = bbox[3] * img_h
#        bbox_w = bbox[4] * img_w
#        bbox_h = bbox[5] * img_h
        bbox_text = "{0} {1:.2f}".format(bbox_name, bbox_conf*100)
        img = drawObject(img, bbox_text, bbox_color, bbox_x, bbox_y, bbox_w, bbox_h)
    
    if writeLabel:
        if not os.path.exists(path_current_label):
            if len(img_labels) > 0:
                try: 
                    f = open(path_current_label, "w") # Open file
                    for cnt, line in enumerate(img_labels): # Go through each line
                        try: 
                            f.write("{} {} {} {} {}".format(line[0], line[2]*img_w, line[3]*img_h, line[4]*img_w, line[5]*img_h))
                            
                        except ValueError:
                            print("Something went wrong writing the label")
                        finally:
                            f.close()
                except ValueError:
                    print("Couldn't open file: " + path_current_label)
        else:
            print("Label file exists or not accessible: " + path_current_label)
        
    
    
    
    # Put path on image
    cv2.putText(img, path_current_img, (20, 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
    
    # Show image with bounding box
    cv2.imshow("LabelChecker", img)
    
    # Wait for keypress
    keyPressed = cv2.waitKey(1) & 0xFF
    
    # Handle keypress
    if keyPressed == 27 or i == len(imgs) - 1: # ESC - Stop running
        cv2.destroyAllWindows()
        break
    
    # Go to next image
    if debug:
        print("Next")
    if not i >= len(imgs) - 1:
            i += 1


#    if keyPressed == ord('k'): # Left - Previous
#        if debug:
#            print("Previous")
#            
#        if not i <= 0:
#            i -= 1
#            
#    elif keyPressed == ord('l'): # Right - Next
#        if debug:
#            print("Next")
#            
#        if not i >= len(imgs) - 1:
#            i += 1
#            
#    elif keyPressed == ord('x'): # X - Delete / move
#        if debug:
#            print("Delete/move")
#            
#        # Remove image from list and get filenames
#        filename_img = imgs.pop(i)
#        filename_label = filename_img[:-4] + ".txt"
#        
#        # Create delete folder if it doesn't exist
#        if not os.path.exists(path_delete):
#            os.mkdir(path_delete)
#        
#        # Get paths
#        path_current_img = os.path.join(path, filename_img)
#        path_current_label = os.path.join(path, filename_label)
#        path_delete_img = os.path.join(path_delete, filename_img)
#        path_delete_label = os.path.join(path_delete, filename_label)
#        
#        # Move image and label
#        os.replace(path_current_img, path_delete_img)
#        os.replace(path_current_label, path_delete_label)
#        print("Moved " + filename_img)
#        
#        # Correct index
#        if  i <= 0:
#            i = 0
#        elif i > len(imgs) - 1:
#            i = len(imgs) - 1
        


