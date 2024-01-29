#!/bin/bash
# Andrea Cumpelik 2024-01-29
# This script is to batch run sfilt3b (eeg generation for downsampled data) for all dat files in a directory.
# Use symlink_par.sh first.

basename="JC283-20220909"

echo $num_dats

for ii in {01..09}; do
	dat_basename="${basename}_${ii}"
	sfilt3b "$dat_basename" eeg

done

echo "Eeg files created successfully."
