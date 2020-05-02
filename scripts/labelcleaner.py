#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 23:09:00 2020

@author: albert
"""
import glob

path = "data/train/box/box00001/"

files = glob.glob(path + "*.txt")

dryRun = False

baddies = 0
for f in files:
    print(str(f))
    if not dryRun:
        lineFix = []
        
        # Read contents of file
        try: 
            fp = open(f, "r") # Open file
            
            for cnt, line in enumerate(fp): # Go through each line
                line = line.strip() # Remove leading and trailing spaces
                
                lineStuff = line.split() # Split into words/numbers
                
                if (float(lineStuff[1]) > 1 or float(lineStuff[1]) < 0 or 
                    float(lineStuff[2]) > 1 or float(lineStuff[2]) < 0 or 
                    float(lineStuff[3]) > 1 or float(lineStuff[3]) < 0 or 
                    float(lineStuff[4]) > 1 or float(lineStuff[4]) < 0):
                    # Fuck this shit
                    print("   Ladies and gentlemen, we got him 🔫")
                    baddies += 1
                else:
                    lineFix.append(lineStuff)
            
        except ValueError:
            print("Couldn't open file for reading...")
        finally:
            fp.close()
        
        print(lineFix)
        # Write new contents
        try: 
            print("opening")
            fp = open(f, "w") # Open file
            
            try: 
                if len(lineFix) > 0:
                    for label in lineFix:
                        ID = int(label[0]) # Class ID
                        x = float(label[1]) # x center
                        y = float(label[2]) # y center
                        w = float(label[3]) # width
                        h = float(label[4]) # height
                        fp.write("{} {} {} {} {}\n".format(ID, x, y, w, h))
                else:
                    fp.write("")
            except ValueError:
                print("Something went wrong writing the label")
        except ValueError:
            print("Couldn't open file for writing...")
        finally:
            fp.close()
print("Number of files: " + str(len(files)))