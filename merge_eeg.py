#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 16:20:31 2024
@author: andrea
This script merges all eeg files for a session and splits them back according to session timestamps. The Jupyer Notebook was made for a single
session, and the Python script is better for multiple sessions.

To run:
cat basenames_subset | xargs -n 2 ./merge_eeg.py
"""

import numpy as np
import os
import csv
import json
import argparse

# Change this based on eeg location
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
print("Now running eeg merging on",basename)

sample_rate_res_old=24000
sample_rate_whl=39.0625
sample_rate_res=20000
sample_rate_eeg=1250
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

# Num tetrodes is fixed
# Jozsef's script for generating eeg files doesn't use the par file; the dead channels still get recorded, so all of them are included
num_channels = 128

# Merge and split eeg files
def find_files_with_eeg(directory):
    eeg_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.eeg'):
                eeg_files.append(os.path.join(root, file))
                
    return eeg_files

if not os.path.isdir(mbasedir):
    os.makedirs(mbasedir)
directory_path_eeg = basedir+"eeg/"+animal_name+'/'+date+'/'

# find all eeg files in a session
eeg_files = sorted(find_files_with_eeg(directory_path_eeg)) # sort the filenames numerically

# initialize a merged eeg file and add the first file to it
eeg_merged=np.fromfile(eeg_files[0], dtype=np.int16)
print('Reshaping',eeg_files[0],'from length',eeg_merged.shape)
# reshape the first file (1D to 2D array) so that each row corresponds to one tetrode
eeg_merged= eeg_merged.reshape(int(len(eeg_merged)/num_channels),num_channels)
print('New eeg_merged shape:',eeg_merged.shape)

# iterate over the other files and add them to the large merged file
for eeg_file_i in range(1,len(eeg_files)):
    eeg_t=np.fromfile(eeg_files[eeg_file_i], dtype=np.int16)
    print('Reshaping',eeg_files[eeg_file_i], 'from length',eeg_t.shape)
    eeg_t= eeg_t.reshape(int(len(eeg_t)/num_channels),num_channels)
    print('New eeg_merged shape:',eeg_t.shape)
    eeg_merged=np.append(eeg_merged,eeg_t,axis=0)

print('Final eeg_merged shape:',eeg_merged.shape)
    
# load the session timestamps and downsample them
session_timestamps=np.loadtxt(basedir+"processing/"+animal_name+'/'+date+'/'+'session_shifts.txt')

session_timestamps=np.append([0],session_timestamps) # start the first timestamp at 0
session_timestamps_down=session_timestamps*downsampled_res
print('Resampled session timestamps:',session_timestamps)

for session_idx_i in range(len(session_idx)):
    # generate reward arms files for the training session files
    if session_names[session_idx_i]=='training1' or session_names[session_idx_i]=='training2':
        np.savetxt(mbasedir+animal_name+'-'+date+'_'+session_names[session_idx_i]+'.reward_arms', reward_arms, fmt='%i',newline=" ")
    
    # cut the eeg files according to the session timestamps and write them to the merged folder
    start_cut=session_idx[session_idx_i][0]-1
    end_cut=session_idx[session_idx_i][-1]
    start_eeg=int(session_timestamps_down[start_cut]/sample_rate_res*sample_rate_eeg)
    end_eeg=int(session_timestamps_down[end_cut]/sample_rate_res*sample_rate_eeg)

    eeg_temp=eeg_merged[start_eeg:end_eeg,:]

    eeg_temp.tofile(mbasedir+animal_name+'-'+date+'_'+session_names[session_idx_i]+'.eeg')
    
print('Done merging eeg files for',basename)
