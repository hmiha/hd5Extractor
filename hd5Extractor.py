#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import h5py
import numpy as np
import cv2

argvs = sys.argv
if len(argvs) <> 3:
    print 'usage: python hd5Extractor.py <h5name> <saveDir>'

h5name = argvs[1]
saveDir = argvs[2]

disparity_scale = 5.

def load_h5():
    try:
        h5file = h5py.File(h5name, 'r')
        print argvs[1], 'is successfully loaded.'
        return h5file

    except IOError:
        print 'IOError:', argvs[1], 'is NONE.'
        sys.exit()

def read_and_save(item):
    print item
    data = h5file[item].value   # Access to the GROUP using .value method
    l = len(data.shape)         # 4 corresponds to a depthmap, 5 corresponds to LFs
    print 'length1 = ', l

    n1, n2 = data.shape[ : 2]
    n = n1 * n2

    for i in xrange(n):
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
            print 'length = ', l
            print 'Unknown filetype...'
            sys.exit()

        fname = str(y) + '_' + str(x) + '.png'
        fpath = os.path.join(saveDir, item, fname)
        cv2.imwrite(fpath, img)
        print fpath, 'is saved'

    return

def textIO():
    path = os.path.join(saveDir, 'profile.txt')
    f = open(path, 'w')
    f.write('disparity_scale =' + str(disparity_scale))
    f.close()
    print path, 'is written'
    return

if __name__ == '__main__':
    h5file = load_h5()

    if os.path.exists(saveDir):
        print 'The directory', saveDir, 'exists.'
        print 'End.'
        sys.exit()
    else:
        os.mkdir(saveDir)

    item_list = [ h5file.items()[i][0] for i in xrange(len(h5file.items()))]
    for item in item_list:
        os.mkdir(os.path.join(saveDir, item))
        read_and_save(item)
    textIO()
