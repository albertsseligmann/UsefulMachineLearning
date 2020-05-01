#!/bin/bash


prefix="cones/data/"
file_paths=`find Train -type f -name "*.jpg"`

for file in $file_paths
do
    echo $prefix$file >> cones.train
done

file_paths=`find Train -type f -name "*.png"`

for file in $file_paths
do
    echo $prefix$file >> cones.train
done

file_paths=`find Crossvalidate -type f -name "*.jpg"`

for file in $file_paths
do
    echo $prefix$file >> cones.valid
done

file_paths=`find Crossvalidate -type f -name "*.png"`

for file in $file_paths
do
    echo $prefix$file >> cones.valid
done
