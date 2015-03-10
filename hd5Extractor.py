#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import h5py
import numpy as np
import cv2

disparity_scale = 5.

def load_h5(h5name):
    try:
        h5file = h5py.File(h5name, 'r')
        #print argvs[1], 'is successfully loaded.'
        return h5file

    except IOError:
        #print 'IOError:', argvs[1], 'is NONE.'
        sys.exit()

def read_and_save(item, data, saveDir, i, n1):
    l = len(data.shape)         # 4 corresponds to a depthmap, 5 corresponds to LFs

    x = i % n1
    y = (i - x) / n1

    if l == 4:
        img = np.array(data[y, x, :, :]) * disparity_scale

    elif l == 5:
        raw_img = np.array(data[y, x, :, :, :])
        # swap RGB to GBR
        img = np.zeros(raw_img.shape)
        img[:, :, 0] = raw_img[:, :, 2].copy()
        img[:, :, 1] = raw_img[:, :, 1].copy()
        img[:, :, 2] = raw_img[:, :, 0].copy()

    else:
        return 'Unknown filetype...'
        sys.exit()

    fname = str(y) + '_' + str(x) + '.png'
    fpath = os.path.join(saveDir, item, fname)
    cv2.imwrite(fpath, img)

    return str(fpath + ' is saved')

def textIO(saveDir):
    path = os.path.join(saveDir, 'profile.txt')
    f = open(path, 'w')
    f.write('disparity_scale =' + str(disparity_scale))
    f.close()
    return
