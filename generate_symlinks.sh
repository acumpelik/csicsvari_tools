#!/bin/bash
# Andrea Cumpelik 2024-01-29
# This is a script to generate symbolic links for a given file type. It looks for clu files matching this file type and extracts the part between
# the basename and the given extension. It uses that to generate symlinks for each clu file.
# Takes in the animal, day, path, and extension with no period

path='/adata_pool/merged/'
ext='par'
animal=$1
day=$2
basename=$animal-$day

cd $path$basename || { echo "Failed to change directory to $path"; exit 1; }

basefile=$basename.$ext

if [[ ! -f $basefile ]]; then
  echo "Base file $basefile does not exist."
  exit 1
fi

echo "Generating symlinks for ${basefile}"

files_full=$(find $path$basename -type f -name $basename_'*.clu')

for file in $files_full; do
	filename=$(basename "$file")
	middle=$(echo "$filename" | sed -E "s|${basename}_(.*)\.clu|\1|")
	ln -s "${basename}.${ext}" "${basename}_${middle}.${ext}"
done
