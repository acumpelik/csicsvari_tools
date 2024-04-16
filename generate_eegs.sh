#!/bin/bash
# Andrea Cumpelik 2024-01-29
# This script is to batch run sfilt3b (eeg generation for downsampled data) for all dat files in a directory.
# First it will use check_len_24_20_div16_resample2_JONb to downsample from 24kHz. to 20kHz.
# Then it will generate .par files for each dat file, and finally it will run sfilt3b.
# Run as data user.

# To run: first edit the path
# ./generate_eegs.sh $animal $day

path="/mnt/adata11/eeg"
animal=$1
day=$2
basename=$animal-$day
nchan=128

# Change to processing directory and count the number of dat files
cd $path/$animal/$day
num_dats=$(find *.dat | wc -w)
echo "The number of dats in $day is $num_dats"

# Make par file in Jozsef's format
cp TEMPLATE.par $basename.par # rename channel template to dat name format
echo $num_dats >> $basename.par # append number of dat files
cat BASELIST >> $basename.par # append list of dat files
echo "" >> $basename.par # append empty line

# there was a colon here that I removed
check_len_24_20_div16_resample2_JONb $nchan
echo ""
echo "Downsampling to 20 kHz completed."

# Generate symbolic links to the new par for each individual dat files
for i in $(seq 1 $num_dats); do
	if [ $i -lt 10 ]; then
		symlink="${basename}_0$i.par"
	else
		symlink="${basename}_$i.par"
	fi

	ln -s "$basename.par" "$symlink"

	# print if success or failure
	if [ $? -eq 0 ]; then
		echo "Symbolic link $symlink created successfully."
	else
		echo "Failed to create symbolic link for $symlink."
	fi
done

# Run sfilt3b to generate eeg files
for i in $(seq 1 $num_dats); do
	if [ $i -lt 10 ]; then
		dat_basename="${basename}_0$i"
	else	
		dat_basename="${basename}_$i"
	fi
	sfilt3b "$dat_basename" eeg
	if [ $? -eq 0 ]; then
		echo "Eeg file for $dat_basename created successfully."
	else
		echo "Failed to generate eeg for $dat_basename."
	fi
done

