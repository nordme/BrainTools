# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 12:05:40 2016

@author: sjjoo
"""

import sys
import mne
import matplotlib.pyplot as plt
from mne.utils import run_subprocess, logger
import os
from os import path as op
import copy
import shutil
import numpy as np
from numpy.random import randn
from scipy import stats as stats
import time
from functools import partial

from mne import set_config
set_config('MNE_MEMMAP_MIN_SIZE', '1M')
set_config('MNE_CACHE_DIR', '.tmp')

mne.set_config('MNE_USE_CUDA', 'true')

this_env = copy.copy(os.environ)
#fs_dir = '/mnt/diskArray/projects/freesurfer'
fs_dir = '/mnt/diskArray/projects/avg_fsurfer'

this_env['SUBJECTS_DIR'] = fs_dir
#this_env['FREESURFER_HOME'] = '/usr/local/freesurfer'

raw_dir = '/mnt/scratch/NLR_MEG4'

os.chdir(raw_dir)

subs = ['NLR_102_RS','NLR_105_BB','NLR_110_HH','NLR_127_AM',
        'NLR_132_WP','NLR_145_AC','NLR_150_MG',
        'NLR_152_TC','NLR_160_EK','NLR_161_AK','NLR_162_EF','NLR_163_LF',
        'NLR_164_SF','NLR_170_GM','NLR_172_TH','NLR_174_HS','NLR_179_GM',
        'NLR_180_ZD','NLR_201_GS','NLR_203_AM',
        'NLR_204_AM','NLR_205_AC','NLR_207_AH','NLR_210_SB','NLR_211_LB',
        'NLR_GB310','NLR_KB218','NLR_GB267','NLR_JB420',
        'NLR_HB275','NLR_GB355'] 

#for n, s in enumerate(subs):
#    run_subprocess(['mne', 'watershed_bem', '--subject', subs[n],'--overwrite'], env=this_env)
    
#    mne.bem.make_watershed_bem(subject = subs[n],subjects_dir=fs_dir,overwrite=True,preflood=20, show=True)
"""USE above code
mri_watershed -h 3 -useSRAS -surf /mnt/diskArray/projects/avg_fsurfer/NLR_205_AC/bem/watershed/NLR_205_AC /mnt/diskArray/projects/avg_fsurfer/NLR_205_AC/mri/T1.mgz /mnt/diskArray/projects/avg_fsurfer/NLR_205_AC/bem/watershed/ws
"""

"""
Run head_surf.m
"""

# Let's take a look...
#for n, s in enumerate(subs):
#    mne.viz.plot_bem(subject=subs[n],subjects_dir=fs_dir,brain_surfaces='white', orientation='coronal')

#for n, s in enumerate(subs):
##    os.chdir(os.path.join(fs_dir,subs[n],'bem'))
#    run_subprocess(['mne', 'make_scalp_surfaces', '--subject', subs[n],
#                    '--overwrite','--no-decimate']) # Disable medium and sparse decimations (dense only)
#                                                    # otherwise, it gives errors

""" Co-register...
mne.gui.coregistration(tabbed=False,subject=subs[0],subjects_dir=fs_dir)
# Recommended way is to use mne coreg from terminal
"""

# Session 2
# subs are synced up with session1 folder names...
#
session2 = ['102_rs160815','105_bb161011','110_hh160809','127_am161004',
       '132_wp161122','145_ac160823','150_mg160825',
       '152_tc160623','160_ek160915','161_ak160916','162_ef160829','163_lf160920',
       '164_sf160920','170_gm160822','172_th160825','174_hs160829','179_gm160913',
       '180_zd160826','201_gs150925','203_am151029',
       '204_am151120','205_ac160202','207_ah160809','210_sb160822','211_lb160823',
       'nlr_gb310170829','nlr_kb218170829','nlr_gb267170911','nlr_jb420170828',
       'nlr_hb275170828','nlr_gb355170907']

#subs = ['NLR_205_AC','NLR_206_LM',
#        'NLR_207_AH','NLR_210_SB','NLR_211_LB'
#        ]
#session1 = ['205_ac151208','205_ac160202',
#            '206_lm151119',
#            '206_lm160113','207_ah160608','207_ah160809','210_sb160822','211_lb160617','211_lb160823'
#            ]

#n_subjects = len(subs)
"""
Forward model...
"""
#sourceFlag = np.ones((n_subjects,1))

#%%
#for n, s in enumerate(session1):
#    os.chdir(os.path.join(raw_dir,session1[n]))
#    
#    if s[0:3] == 'nlr':
#        subject = s[0:9].upper()
#    else:
#        subject = 'NLR_' + s[0:6].upper()
#    
#    os.chdir('inverse')
#    fn = 'All_40-sss_eq_'+session1[n]+'-ave.fif'
#    evoked = mne.read_evokeds(fn, condition=0, 
#                              baseline=(None,0), kind='average', proj=True)
#    
#    info = evoked.info 
#    
#    if os.path.isdir('../forward'):
#        os.chdir('../forward')
##    else:
##        temp_src = '/mnt/scratch/NLR_MEG2/' + session1[n] + '/forward'
##        temp_dest = '/mnt/scratch/NLR_MEG3/' + session1[n] + '/forward'
##        shutil.copytree(temp_src, temp_dest)
#    trans = session1[n] + '-trans.fif'
##    Take a look at the sensors
#    mne.viz.plot_trans(info, trans, subject=subs[n], dig=True,
#                       meg_sensors=True, subjects_dir=fs_dir)

#%%
#n = 0
#os.chdir(os.path.join(raw_dir,session1[n]))
#os.chdir('raw_fif')
#pos = mne.chpi.read_head_pos('102_rs160618_1_raw.pos')
#mne.viz.plot_head_positions(pos, mode='traces')

#%%
for n, s in enumerate(session2):
    os.chdir(os.path.join(raw_dir,session2[n]))
    
    if s[0:3] == 'nlr':
        subject = s[0:9].upper()
    else:
        subject = 'NLR_' + s[0:6].upper()
    
    os.chdir('inverse')
    fn = 'All_40-sss_eq_'+session2[n]+'-ave.fif'
    evoked = mne.read_evokeds(fn, condition=0, 
                              baseline=(None,0), kind='average', proj=True)
    
    info = evoked.info 
    
    if os.path.isdir('../forward'):
        os.chdir('../forward')
    else:
        temp_src = '/mnt/scratch/NLR_MEG2/' + session2[n] + '/forward'
        temp_dest = '/mnt/scratch/NLR_MEG3/' + session2[n] + '/forward'
        shutil.copytree(temp_src, temp_dest)
    trans = session2[n] + '-trans.fif'
    
    # Take a look at the sensors
#    mne.viz.plot_trans(info, trans, subject=subs[n], dig=True,
#                       meg_sensors=True, subjects_dir=fs_dir)
                       
    ### Read source space
#    spacing='oct6' #'ico5' # 10242 * 2
    fn2 = subject + '-' + 'ico-5' + '-src.fif' # ico-5
    if s == '205_ac151123' or s == '205_ac160202' or s == 'nlr_jb227170811': # NLR_205 has too small head for ico-5
        fn2 = subject + '-' + 'oct-6' + '-src.fif'

    os.chdir(os.path.join(fs_dir,subject,'bem'))
    src = mne.read_source_spaces(fn2)
    os.chdir(os.path.join(raw_dir,session2[n]))
    os.chdir('forward')
        
    #import numpy as np  # noqa
    #from mayavi import mlab  # noqa
    #from surfer import Brain  # noqa
    #
    #brain = Brain('sample', 'lh', 'inflated', subjects_dir=subjects_dir)
    #surf = brain._geo
    #
    #vertidx = np.where(src[0]['inuse'])[0]
    #
    #mlab.points3d(surf.x[vertidx], surf.y[vertidx],
    #              surf.z[vertidx], color=(1, 1, 0), scale_factor=1.5)
    
    # Create BEM model
    conductivity = (0.3,)  # for single layer
    #conductivity = (0.3, 0.006, 0.3)  # for three layers
    model = mne.make_bem_model(subject=subject, ico=5, # 5=20484, 4=5120
                               conductivity=conductivity, 
                               subjects_dir=fs_dir)
    bem = mne.make_bem_solution(model)
    fn = session2[n] + '-bem-sol.fif'
    mne.write_bem_solution(fn,bem)
    
    # Now create forward model
    fwd = mne.make_forward_solution(info, trans=trans, src=src, bem=bem,
                                    meg=True, eeg=False, mindist=3.0, n_jobs=18)
    fwd = mne.convert_forward_solution(fwd, surf_ori=True, force_fixed=True, copy=True)
    fn = session2[n] + '-sss-fwd.fif'
    mne.write_forward_solution(fn,fwd,overwrite=True)
    
    #Inverse here
#    os.chdir('../covariance')
#    fn = session1[n] + '-40-sss-cov.fif'
#    cov = mne.read_cov(fn)
#    
#    os.chdir('../inverse')
#    # Free: loose = 1; Loose: loose = 0.2
#    inv = mne.minimum_norm.make_inverse_operator(info, fwd, cov, loose=0., depth=0.8, use_cps=True)
#    
#    fn = session1[n] + '-fixed-depth8-inv.fif'
#    mne.minimum_norm.write_inverse_operator(fn,inv)
