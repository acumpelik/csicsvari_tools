#!/bin/bash
# Andrea Cumpelik 2024-01-29
# This is a script to generate symbolic links from the main par files to par files matching the 
# JC..01.* convention. For usage with sfilt3b for example.

# Edit this each time:
base_par="JC283-20220909.par"

# Edit num dats
for ii in {01..09}; do
	symlink="${base_par%.*}_$ii.par"
	ln -s "$base_par" "$symlink"
done

echo "Symbolic links created successfully."
