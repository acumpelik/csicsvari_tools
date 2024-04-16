#!/bin/bash

# This code will count the number of dat files in a directory
# Then it will regenerate the basenames using the directory name, including a leading zero when <=9.

# Set parameters
animal=$1
dir="/adata_pool/processing"
day=$2

cd $dir/$animal/$day

num_dats=$(find *.dat | wc -w)
echo "The number of dats in $day is $num_dats"
