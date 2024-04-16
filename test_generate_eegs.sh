#!/bin/bash

# This code will count the number of dat files in a directory
# Then it will regenerate the basenames using the directory name, including a leading zero when <=9.

# Set parameters
animal=$1
day=$2
dir="/adata_pool/preprocessing"

cd $dir/$animal/$day

num_dats=$(find *.dat | wc -w)
echo "The number of dats in $day is $num_dats"


for i in $(seq 1 $num_dats)
do
	if [ $i -lt 10 ]; then
		echo "$animal-$day"_0"$i"
	else
		echo "$animal-$day"_"$i"
	fi
done
