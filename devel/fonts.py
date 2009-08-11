#!/usr/bin/python

import os
import glob

def getfonts (dir='../fonts/', mkvmerge=0):
    """Returns a list of all the fonts in a directory.
    
    Accepts only one directory at a time."""
    
    # Check if dir exists, if not, ask another
    while os.path.isdir(dir) == False:
        dir = raw_input("Dir doesn't exist. Write another: ")
        if dir[-1] == '\r':
            dir = dir[:-1]
    
    fonts = glob.glob(os.path.abspath(dir + '*.?tf'))
    
    if glob.glob('*.?tf'):
        localfonts = glob.glob('*.?tf')
        fonts += localfonts
    
    # Fill the fonts list with the absolute paths of the fonts
    if mkvmerge == 1:
        
        mkvfonts = []
        
        for font in fonts:
            mkvfonts.append(' --attachment-mime-type application/x-truetype-font --attachment-name ' + font[9:] + ' --attach-file ' + font)
        
        return mkvfonts
    
    return fonts                

if __name__ == '__main__':
	print(getfonts())
