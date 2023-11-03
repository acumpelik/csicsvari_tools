#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 08:56:49 2023

@author: acumpeli
"""

labels = ['pp', 'p1', 'pr', 'b1', 'bp']



# 
for cell_i in range(len(labels)):
    #######################################################################
    cell_type = labels[cell_i][0]
    brain_region=labels[cell_i][1]
    label = labels[cell_i]
    if tet_i<last_pfc_left:
        des.append(label)
        des_full.append('pfc_left')
    elif tet_i<last_pfc_right:
        des.append(label)
        des_full.append('pfc_right')
    else:
        des.append(label)
        des_full.append('hpc_right')


    # if neurontype_i[0][0][0]=='b': # if cell type is interneuron/basket
        # if tet_i<last_pfc_left:
        #     des.append('bp')
        #     des_full.append('pfc_left')
        # elif tet_i<last_pfc_right:
        #     des.append('bp')
        #     des_full.append('pfc_right')
        # else:
        #     des.append('b1')
        #     des_full.append('hpc_right')
    # elif neurontype_i[0][0][1]=='p': # if cell type is pyramidal
    #     if tet_i<last_pfc_left:
    #         des.append('pp')
    #         des_full.append('pfc_left')
    #     elif tet_i<last_pfc_right:
    #         des.append('pp')
    #         des_full.append('pfc_right')
    #     else:
    #         des.append('p1')
    #         des_full.append('hpc_right')