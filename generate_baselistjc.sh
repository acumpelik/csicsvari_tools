#!/bin/bash
# Andrea 2024-07-25
# This script cd's to a dir and generates a par file in Jozsef's format
# It requires a TEMPLATE.par, BASELIST, and the number of dat files

# Change to processing directory and count the number of dat files

input_path='/adata_pool/preprocessing'
animal=$1
day=$2
output_path='/adata_pool/merged'

basename=$animal-$day

cd $input_path/$animal/$day
num_dats=$(find *.dat | wc -w)
echo "The number of dats is $num_dats"

# Make par file in Jozsef's format
cp TEMPLATE.par $basename.par # rename channel template to dat name format
echo $num_dats >> $basename.par # append number of dat files
cat BASELIST >> $basename.par # append list of dat files
echo "" >> $basename.par # append empty line

echo Copying $input_path/$animal/$day/$basename.par to $output_path/$basename/
cp $input_path/$animal/$day/$basename.par $output_path/$basename/
