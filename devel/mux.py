#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Created on 2009/08/27

@author: Ricardo
'''

import os
import glob

def getfonts(dir='../fonts/'):
    """Returns a list of all the fonts in a directory.
    
    Accepts only one directory at a time."""
    
    # Check if directory exists, if not, ask another
    while os.path.isdir(dir) == False:
        dir = input("That directory doesn't exist. Write another: ")
        if dir[-1] == '\r':
            dir = dir[:-1]
    
    fonts = glob.glob(os.path.abspath(dir + '*.?tf'))
    
    if glob.glob('*.?tf'):
        localfonts = glob.glob('*.?tf')
        fonts += localfonts
    
    mkvfonts = []
    
    for font in fonts:
        mkvfonts.append(' --attachment-mime-type application/x-truetype-font --attachment-name ' + font[9:] + ' --attach-file ' + font)
    
    return mkvfonts


if __name__ == '__main__':
    pass