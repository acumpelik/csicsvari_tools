#!/bin/bash
# 2024-03-31
# Script to convert several bin files to dat files in the current directory.

animal="JC315"
day="20240330"
numbin=6 #number of bin files

basename=$animal-$day

for i in `seq 1 $numbin`; do
	Axona2dat3_15_128 $basename"_0"$i".bin"
done 
