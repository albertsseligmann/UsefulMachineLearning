#!/bin/bash

for file in `find ~/Downloads/FSOCO-Data -type f | awk 'NR %100 == 0'`; do 
	cp $file ~/Downloads/FSOCO-Data/_Crossvalidation
done
