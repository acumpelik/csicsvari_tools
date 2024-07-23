#!/bin/bash
# Andrea Cumpelik 2024-05-24
# This script is to batch run fextrcomprbb3 (eegh generation for downsampled data) for all dat files in a directory.
# It was created after generate_eegs.sh, and assumes a par file in Jozsef's format and downsampled dats are already generated.
# Run as data user.

# To run: first edit the path
# ./generate_eegh.sh $animal $day

# To run for multiple sessions, create a basenames file with animal and day on each line. Then run:
# cat basenames | xargs -n 2 ./generate_eegh.sh

path="/adata_clust/eeg"
animal=$1
day=$2
basename=$animal-$day
nchan=128

echo "Now running eegh conversion on $basename."

# Change to processing directory and count the number of dat files
cd $path/$animal/$day
num_dats=$(find *.dat | wc -w)
echo "The number of dats is $num_dats"

# Run fextrcomprbb3 to generate eegh files
for i in $(seq 1 $num_dats); do
	if [ $i -lt 10 ]; then
		dat_basename="${basename}_0$i"
	else	
		dat_basename="${basename}_$i"
	fi
	fextrcomprbb3 "$dat_basename"
	if [ $? -eq 0 ]; then
		echo "Eegh file for $dat_basename created successfully."
	else
		echo "Failed to generate eegh for $dat_basename."
	fi
done

