#!/bin/bash
# Andrea 2024-07-24
# This script is to copy the desel or other file from the current dir to all sessions dirs and rename it with the corresponding basename.

animal=$1
day=$2
origin_path='/mnt/adata11/processing/'
dest_path='/adata_pool/merged'
basename=$animal-$day
ext='desel'

#echo 'Copying' $basename.desel

cp $animal.desel $dest_path/$basename/$basename.desel
