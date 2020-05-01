#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script used for checking for duplicate fileNAMES in two given directories.
Optionally delete the files in one directory.

Author: Albert Seligmann - 26/06/2019
"""

import os
import glob
import fileinput
import sys
import argparse


def checkDir(thisdir, otherdir, extension):
    files_here = glob.glob(thisdir + "*." + extension)
    files_there = glob.glob(otherdir + "*." + extension)
    names_here = []
    names_there = []
    
    for f in files_here:
        names_here.append(os.path.basename(f))
    
    for f in files_there:
        names_there.append(os.path.basename(f))
    
    duplicates = set(names_here).intersection(names_there)
        
    print("This dir: " + thisdir)
    print(" - Files here: " + str(len(files_here)))
    
    print("Other dir: " + otherdir)
    print(" - Files there: " + str(len(files_there)))
    
    print("Number of duplicates: " + str(len(duplicates)))
    
    
    i = 1
    for f in duplicates:
        print(f)
        i += 1

def delFile(file):
    print("x")

parser = argparse.ArgumentParser()
parser.add_argument("odir", help="other directory relative to CWD")

args = parser.parse_args()

cur_dir = os.getcwd() + "/"

checkDir(cur_dir, args.odir, "txt")