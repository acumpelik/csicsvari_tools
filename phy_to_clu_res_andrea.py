#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

import matplotlib.pyplot as plt

from scipy import interpolate


# In[2]:


# Data_dir="/mnt/adata9/processing/"
Data_dir = "/home/acumpeli/adata_laptop/mnt/adata9/processing/"



sample_rate_whl=39.0625
sample_rate_res=20000

sample_rate_res_old=24000

all_session_name=['presleep','training1','intersleep','training2','postsleep']

downsample_res=sample_rate_res/sample_rate_res_old


# In[10]:


animal_name='JC283'
date='20220910'

mData_dir="/home/acumpeli/adata_laptop/mnt/adata9/merged/m"+animal_name+'-'+date+'/'
if not os.path.isdir(mData_dir):
        os.makedirs(mData_dir)

num_tetrodes=25
last_pfc_left=8
last_pfc_right=15

session_idx=[[1],[2,3,4],[5],[6],[7]]


mfolder=Data_dir+animal_name+'/m'+animal_name+'-'+date+'/'

cell_ind=2

res=np.zeros([0])
clu=np.zeros([0])
des=[]

des_full=[]


for tet_i in range(num_tetrodes):
    #print("processing tet"+str(tet_i))
    folder=Data_dir+animal_name+'/'+date+'/sorted/tet'+str(tet_i)+'/phy_export/'
    print(tet_i)
    #################
    ### If tetrode folder exists, continue:
    #################
    if os.path.isdir(folder)==True:
        print('folder exists')
        ############################################
        spike_clusters=np.load(folder+'spike_clusters.npy')
        spike_times=np.load(folder+'spike_times.npy')

        good_noise=pd.read_csv(folder+'cluster_group.tsv',sep='\t').to_numpy()

        good_ind=np.zeros([0])
        mua_ind=np.zeros([0])
        for i in range(good_noise.shape[0]):
            if good_noise[i,1]=='good' or good_noise[i,1]=='mua':
                neurontype=pd.read_csv(folder+'cluster_neurontype.tsv',sep='\t').to_numpy()
                good_ind=np.append(good_ind,good_noise[i,0])
                if good_noise[i,1]=='mua':
                    mua_ind=np.append(mua_ind,1)
                else:
                    mua_ind=np.append(mua_ind,0)


        for cell_i in range(len(good_ind)):
            
            itemindex = np.where(neurontype[:,0] == good_ind[cell_i])
            neurontype_i=neurontype[itemindex,1][0][0]
            
            ############################################
            # Check brain region
            ############################################
            brain_regions = ['1', 'p' or 'r' or 'o' or 'c']
            cell_types = ['b', 'p']
            if neurontype_i[0] in cell_types and neurontype_i[1] in brain_regions:
                des.append(neurontype_i)
                if tet_i<last_pfc_left:
                    des_full.append('pfc_left')
                elif tet_i<last_pfc_right:
                    des_full.append('pfc_right')
                else:
                    des_full.append('hpc_right')
            else:
                print('check label for cluster', cell_i)
                break


            res_t=spike_times[spike_clusters==good_ind[cell_i]]
            clu_t=cell_ind*np.ones(len(res_t))

            if mua_ind[cell_i]==1:
                clu_t=np.ones(len(clu_t))

            res=np.append(res,res_t)
            clu=np.append(clu,clu_t)

            cell_ind=cell_ind+1
            
        ##########################################
    else:
        print('folder missing')

# whl new creation

session_shift=np.loadtxt(Data_dir+animal_name+'/'+date+'/'+'session_shifts.txt')
session_shift=np.append([0],session_shift)




df = pd.read_csv(Data_dir+animal_name+'/'+date+'/'+date+'.whl',
                                        sep=' ', header=None, names=['dim1', 'dim2', 'dim1_2', 'dim2_2', 'timestamp','valid'])

whl_old=pd.DataFrame(df).to_numpy()
length_time_whl=whl_old.shape[0]/50/60/60

len_session=session_shift[-1]
length_time=len_session/sample_rate_res_old/60/60

data_points_len=(len_session)/whl_old.shape[0]
sample_rate_whl_old=data_points_len/sample_rate_res_old


sample_rate_whl_old=1/sample_rate_whl_old



x_old=np.linspace(0,len_session,whl_old.shape[0])
x_new=np.linspace(0,len_session,int(whl_old.shape[0]/sample_rate_whl_old*sample_rate_whl))

whl_new=np.zeros([len(x_new),2])

#dim1
f = interpolate.interp1d(x_old, whl_old[:,0])
y_new=f(x_new)
whl_new[:,0] = f(x_new)
#dim2
f = interpolate.interp1d(x_old, whl_old[:,1])
whl_new[:,1] = f(x_new)

#add -1 for missing
index_bad_new=np.zeros(len(x_new))
for i in range(whl_old.shape[0]):
    if whl_old[i,0]==1023:
        i_new=int(i/sample_rate_whl_old*sample_rate_whl)
        if i_new+1>len(index_bad_new)-1:
            index_bad_new[i_new-1:i_new]=1
        else:
            index_bad_new[i_new-2:i_new+2]=1


whl_new[index_bad_new>0,:]=1023


#np.savetxt(mfolder+animal_name+'-'+date+'_'+str(session_i)+'.whl', whl_new.astype(int), fmt='%i')



sort_arg=np.argsort(res)

res=res[sort_arg]
clu=clu[sort_arg]

res_down=res*downsample_res
session_shift_down=session_shift*downsample_res

##########################
print(session_shift_down)

for i in range(len(session_idx)):

    start_cut=session_idx[i][0]-1
    end_cut=session_idx[i][-1]
    
    ##############################################################
    print(start_cut, end_cut)
    print(session_idx)
    
    index1=res_down<session_shift_down[end_cut]
    index2=res_down>session_shift_down[start_cut]
    #test=np.logical_and(index1,index2)
    clu_temp=clu[np.logical_and(res_down<session_shift_down[end_cut],res_down>session_shift_down[start_cut])]
    res_temp=res_down[np.logical_and(res_down<session_shift_down[end_cut],res_down>session_shift_down[start_cut])]

    res_temp=res_temp-session_shift_down[start_cut]
    clu_temp = np.insert(clu_temp, 0, cell_ind, axis=0)


    np.savetxt(mData_dir+animal_name+'-'+date+'_'+all_session_name[i]+'.res', res_temp.astype(int), fmt='%i')
    np.savetxt(mData_dir+animal_name+'-'+date+'_'+all_session_name[i]+'.clu', clu_temp.astype(int), fmt='%i')

    start_whl=int(session_shift_down[start_cut]/sample_rate_res*sample_rate_whl)
    end_whl=int(session_shift_down[end_cut]/sample_rate_res*sample_rate_whl)
    whl_temp=whl_new[start_whl:end_whl]

    np.savetxt(mData_dir+animal_name+'-'+date+'_'+all_session_name[i]+'.whl', whl_temp.astype(int), fmt='%i')

    plt.plot(whl_temp[:,0],whl_temp[:,1],'*')
    plt.xlim([0,200])
    plt.ylim([0,200])
    plt.show()



with open(mData_dir+animal_name+'-'+date+'.des', 'w') as fp:
    fp.write('\n'.join(des))

with open(mData_dir+animal_name+'-'+date+'.des_full', 'w') as fp:
    fp.write('\n'.join(des_full))


# In[ ]:




