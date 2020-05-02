#!/bin/bash

# Run from main project dir

prefix_list="detector/cfg"
prefix_data="../"
file_paths=`find data/train -type f -name "*.jpg"`

for file in $file_paths
do
    echo $prefix_data$file >> $prefix_list/yolo31392.train
done

file_paths=`find data/train -type f -name "*.png"`

for file in $file_paths
do
    echo $prefix_data$file >> $prefix_list/yolo31392.train
done

file_paths=`find data/valid -type f -name "*.jpg"`

for file in $file_paths
do
    echo $prefix_data$file >> $prefix_list/yolo31392.valid
done

file_paths=`find data/valid -type f -name "*.png"`

for file in $file_paths
do
    echo $prefix_data$file >> $prefix_list/yolo31392.valid
done
