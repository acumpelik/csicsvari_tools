#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 16:20:31 2024
@author: andrea
This script merges all eeg files for a session and splits them back according to session timestamps. The Jupyer Notebook was made for a single
session, and the Python script is better for multiple sessions.

To run:
cat basenames_subset | xargs -n 2 ./merge_eegh.py
"""

import numpy as np
import os
import csv
import json
import argparse

# Change this based on eegh location
basedir = "/mnt/adata9/"

# Import basename
parser = argparse.ArgumentParser()
parser.add_argument('animal_name')
parser.add_argument('date')
args=parser.parse_args()

animal_name=args.animal_name
date=args.date
basename = animal_name+'-'+date

# These parameters may change
mbasedir="/adata_pool/merged/"+basename+'/'
print("Now running eegh merging on",basename)

sample_rate_res_old=24000
sample_rate_whl=39.0625
sample_rate_res=20000
sample_rate_eegh=5000
downsampled_res=sample_rate_res/sample_rate_res_old

# Import session metadata
session_metadata = {}
with open('session_metadata.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=";")    
    for line in reader:
        session_id = line.pop('session_id')
        session_metadata[session_id] = line
        


# Read metadata
num_tetrodes = int(session_metadata[basename]['num_tetr'])
session_idx = json.loads(session_metadata[basename]['session_idx'])
session_names_str = session_metadata[basename]['session_names']
session_names_str = session_names_str.replace("'",'"') # the single quotes aren't being read in JSON, but I can't use " in the csv because it's a str delimiter
session_names = json.loads(session_names_str)
reward_arms_str = session_metadata[basename]['reward_arms']
reward_arms = np.array(list(map(int, reward_arms_str.split(','))))

# Merge and split eegh files
def find_files_with_eegh(directory):
    eegh_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if 'eegh' in file:
                eegh_files.append(os.path.join(root, file))
                
    return eegh_files

if not os.path.isdir(mbasedir):
    os.makedirs(mbasedir)
directory_path_eegh = basedir+"eeg/"+animal_name+'/'+date+'/'

# find all eegh files in a session
eegh_files = sorted(find_files_with_eegh(directory_path_eegh)) # sort the filenames numerically
print('Found eegh files:')
for file in eegh_files:
    print(file)

# initialize a merged eegh file and add the first file to it
eegh_merged=np.fromfile(eegh_files[0], dtype=np.int16)
# reshape the first file (1D to 2D array) so that each row corresponds to one tetrode
eegh_merged= eegh_merged.reshape(int(len(eegh_merged)/num_tetrodes),num_tetrodes)

# iterate over the other files and add them to the large merged file
for eegh_file_i in range(1,len(eegh_files)):
    eegh_t=np.fromfile(eegh_files[eegh_file_i], dtype=np.int16)
    eegh_t= eegh_t.reshape(int(len(eegh_t)/num_tetrodes),num_tetrodes)
    eegh_merged=np.append(eegh_merged,eegh_t,axis=0)

# calculate the total length (num timestamps) of the merged eegh file
length_eegh_merged=eegh_merged.shape[0]

# load the session timestamps and downsample them
session_timestamps=np.loadtxt(basedir+"processing/"+animal_name+'/'+date+'/'+'session_shifts.txt')
session_timestamps=np.append([0],session_timestamps) # start the first timestamp at 0
session_timestamps_down=session_timestamps*downsampled_res


for session_idx_i in range(len(session_idx)):
    # generate reward arms files for the training session files
    if session_names[session_idx_i]=='training1' or session_names[session_idx_i]=='training2':
        np.savetxt(mbasedir+animal_name+'-'+date+'_'+session_names[session_idx_i]+'.reward_arms', reward_arms, fmt='%i',newline=" ")
    
    # cut the eegh files according to the session timestamps and write them to the merged folder
    start_cut=session_idx[session_idx_i][0]-1
    end_cut=session_idx[session_idx_i][-1]
    start_eegh=int(session_timestamps_down[start_cut]/sample_rate_res*sample_rate_eegh)
    end_eegh=int(session_timestamps_down[end_cut]/sample_rate_res*sample_rate_eegh)

    eegh_temp=eegh_merged[start_eegh:end_eegh,:]

    eegh_temp.tofile(mbasedir+animal_name+'-'+date+'_'+session_names[session_idx_i]+'.eegh')
    