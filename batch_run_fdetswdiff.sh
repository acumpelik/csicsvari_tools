#!/bin/bash
# Andrea 2024-07-25 This script was written to batch run Jozsef's script fdetswdiff, but can be modified to run other scripts.

# cd to directory of choice
# name eeg files in dir
# Iterate over eeg files
# Run bash fdetswdiff_andrea JC315-20240402_intersleep

path='/adata_pool/merged/'
animal=$1
day=$2
ext='eeg'
basename=$animal-$day
script_name='fdetswdiff_andrea'

cd $path$basename || { echo "Failed to change directory to $path"; exit 1; }
echo "Now running ${script_nam} in ${pwd}"

files_full=$(find "$path$basename" -type f -name "$basename_*$ext")

for file in $files_full; do
        filename=$(basename "$file")
	if [[ ! -f $filename ]]; then
  		echo "Base file $basefile does not exist."
		exit 1
	fi
        basefilename=$(basename "$file")
        middle=$(echo "$basefilename" | sed -E "s|${basename}_(.*)\.$ext|\1|")
	filename="${basename}_${middle}"
	echo "Running ${script_name} on ${filename}"
	bash $script_name $filename
done      
