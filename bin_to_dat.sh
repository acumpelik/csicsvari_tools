#!/bin/bash
# 2024-03-31
# Script to convert several bin files to dat files in the current directory.

# Find animal and day from path
animal=$(pwd | rev | cut -c 10-14 | rev)
day=$(pwd | rev | cut -c 1-8 | rev)

# Count bin files
numbin=$(find *.bin | wc -w)

basename=$animal-$day

for i in $(seq 1 $numbin); do
	if [ $i -lt 10 ]; then
		Axona2dat3_15_128 $basename"_0"$i".bin"
	else	
		Axona2dat3_15_128 $basename"_"$i".bin"
	fi
done 
