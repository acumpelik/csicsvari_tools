#!/bin/bash
# Andrea Cumpelik 2024-01-29
# This script is to batch run sfilt3b (eeg generation for downsampled data) for all dat files in a directory.
# First it will use check_len_24_20_div16_resample2_JONb to downsample from 24kHz. to 20kHz.
# Then it will generate .par files for each dat file, and finally it will run sfilt3b.
# Run as data user.

basename=$1
nchan=128
num_dats=$2 # with leading zero

cp TEMPLATE.par $basename.par # rename channel template to dat name format
echo ${num_dats#"0"} >> $basename.par # add number of dat files, omit leading zero
cat BASELIST >> $basename.par # add list of files
echo "" >> $basename.par # add empty line
:
check_len_24_20_div16_resample2_JONb $nchan
echo ""
echo "Downsampling to 20 kHz completed."

# Edit num dats
for ii in {01..04}; do
	symlink="${basename}_$ii.par"
	ln -s "$basename.par" "$symlink"

	# print if success or failure
	if [ $? -eq 0 ]; then
		echo "Symbolic link $symlink created successfully."
	else
		echo "Failed to create symbolic link for $symlink."
	fi
done

for ii in {01..04}; do
	dat_basename="${basename}_${ii}"
	sfilt3b "$dat_basename" eeg
	if [ $? -eq 0 ]; then
		echo "Eeg file for $dat_basename created successfully."
	else
		echo "Failed to generate eeg for $dat_basename."
	fi
done

