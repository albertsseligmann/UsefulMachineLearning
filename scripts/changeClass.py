# -*- coding: utf-8 -*-
"""
Script used for changing the YOLO class of all files in a directory.
Set the correct classes and run the file from the directory containing files to be changed.

Author: Albert Seligmann - 26/06/2019
"""

import os
import glob
import fileinput
import sys


def changeClass(mydir, b_f, b_t, y_f, y_t, o_f, o_t, o_big_f, o_big_t, g_f, g_t):
    files = glob.glob(mydir + "*.txt")
    
    i = 1
    for f in files:
        print(f)
        changeLine(f, b_f, b_t, y_f, y_t, o_f, o_t, o_big_f, o_big_t, g_f, g_t)
        i += 1
    print("Number of files: " + str(len(files)))

def changeLine(file, b_f, b_t, y_f, y_t, o_f, o_t, o_big_f, o_big_t, g_f, g_t):
    for line in fileinput.input([file], inplace=True):
        temp_line = list(line)
        
        if temp_line[0] == b_f:
            temp_line[0] = b_t
        elif temp_line[0] == y_f:
            temp_line[0] = y_t
        elif temp_line[0] == o_f:
            temp_line[0] = o_t
        elif temp_line[0] == o_big_f:
            temp_line[0] = o_big_t
        elif temp_line[0] == g_f:
            temp_line[0] = g_t
        
        new_line = "".join(temp_line)
        sys.stdout.write(new_line)
    

blue_from = '0'
yellow_from = '1'
orange_from = 'x'
orange_big_from = '2'
green_from = 'x'

blue_to = '0'
yellow_to = '1'
orange_to = '2'
orange_big_to = '3'
green_to = '4'

cur_dir = os.getcwd() + "/"

print("dir = " + cur_dir)

changeClass(cur_dir, blue_from, blue_to, yellow_from, yellow_to, orange_from, orange_to, orange_big_from, orange_big_to, green_from, green_to)