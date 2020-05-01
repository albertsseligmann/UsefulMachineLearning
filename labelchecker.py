#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 12:03:01 2020

@author: albert
"""

import sys
import os
import cv2

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





### LabelChecker ###
# args: path to folder
# Opens window with bounding boxes drawn as overlay. User navigates with the
# K and L keys and can press X to move img to /delete/. Press ESC to stop.

debug = False

# Initialise path variable for arguments
path = ""

# Handle arguments
if (
    any([arg == "-h" for arg in sys.argv])
    or len(sys.argv) != 2
    or not os.path.exists(sys.argv[1])
):
    print(
        "\n\nUsage:\n python <filename> <full path>"
    )
    print("Example:\n python src/labelchecker.py train/books/book00000")
    print("\n\n")
    exit()
else:
    print("L = Next image, K = Previous image, X = Delete/move image, ESC = Exit")
    path = sys.argv[1]

# Define constants
classNameID = {"Box": 269, "Book": 68, "Cup": 56}
classIDName = {269: "Box", 68: "Book", 56: "Cup"}
classIDColor = {269: (255, 0, 0), 68: (0, 255, 0), 56: (0, 0, 255)}

# Define where to move "deleted" images
delete_folder = "delete"
path_delete = os.path.join(path, delete_folder)

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
        print(path_current_img)
    
    # Initialise list
    img_labels = []
    try: 
        f = open(path_current_label, "r") # Open file
        for cnt, line in enumerate(f): # Go through each line
            line = line.strip() # Remove leading and trailing spaces
            
            if debug:
                print("Label {}: {}".format(cnt, line))
                
            lineStuff = line.split() # Split into words/numbers
            
            try: 
                # Read label information
                ID = int(lineStuff[0]) # Class ID
                x = float(lineStuff[1]) # x center
                y = float(lineStuff[2]) # y center
                w = float(lineStuff[3]) # width
                h = float(lineStuff[4]) # height
                
                # Add label information to list
                this_label = [ID, x, y, w, h]
                img_labels.append(this_label)
                
            except ValueError:
                print("Something went wrong with the label")
                
    except IOError:
        print("Label file not accessible")
        
    finally:
        f.close()
    
    # Get image dimensions
    img_dim = img.shape
    img_h = img_dim[0]
    img_w = img_dim[1]
    img_c = img_dim[2]
    
    # Draw bounding box
    for bbox in img_labels:
        bbox_name = classIDName[bbox[0]] # Get name and color form ID
        bbox_color = classIDColor[bbox[0]]
        bbox_x = bbox[1] * img_w # Go from relative to absolute
        bbox_y = bbox[2] * img_h
        bbox_w = bbox[3] * img_w
        bbox_h = bbox[4] * img_h
        img = drawObject(img, bbox_name, bbox_color, bbox_x, bbox_y, bbox_w, bbox_h)
    
    # Put path on image
    cv2.putText(img, path_current_img, (20, 20), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
    
    # Show image with bounding box
    cv2.imshow("LabelChecker", img)
    
    # Wait for keypress
    keyPressed = cv2.waitKey(0) & 0xFF
    
    # Handle keypress
    if keyPressed == 27: # ESC - Stop running
        cv2.destroyAllWindows()
        break
    if keyPressed == ord('k'): # Left - Previous
        if debug:
            print("Previous")
            
        if not i <= 0:
            i -= 1
            
    elif keyPressed == ord('l'): # Right - Next
        if debug:
            print("Next")
            
        if not i >= len(imgs) - 1:
            i += 1
            
    elif keyPressed == ord('x'): # X - Delete / move
        if debug:
            print("Delete/move")
            
        # Remove image from list and get filenames
        filename_img = imgs.pop(i)
        filename_label = filename_img[:-4] + ".txt"
        
        # Create delete folder if it doesn't exist
        if not os.path.exists(path_delete):
            os.mkdir(path_delete)
        
        # Get paths
        path_current_img = os.path.join(path, filename_img)
        path_current_label = os.path.join(path, filename_label)
        path_delete_img = os.path.join(path_delete, filename_img)
        path_delete_label = os.path.join(path_delete, filename_label)
        
        # Move image and label
        os.replace(path_current_img, path_delete_img)
        os.replace(path_current_label, path_delete_label)
        print("Moved " + filename_img)
        
        # Correct index
        if  i <= 0:
            i = 0
        elif i > len(imgs) - 1:
            i = len(imgs) - 1
        
