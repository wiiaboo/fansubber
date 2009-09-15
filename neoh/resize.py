#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Resize Script
# by RiCON <wiiaboo@gmail.com>
# Scans current dir for mkv/mp4/avi and resizes each to 576p

# Imports
from os import path, rename, mkdir, name, system, remove
import glob
from time import asctime

# Config
done            = path.abspath('done')
logFile         = "resize.log"
x264            = 'x264'
x264opts        = '--preset slow --tune animation --level 4.1 --crf 18'
removeTempFiles = False
test            = False

# Program
if path.isdir(done) == 'False':
    mkdir(done)
    print('Dir "done" criado')

def write_log(self, close=False):
    '''Reports to an external log or to screen'''
    output = "{} => {}".format(asctime(), self)
    if logFile:
        if not path.isfile(logFile):
            log = open(logFile,"w")
        else:
            log = open(logFile,"a")
        print(output,file=log)
        if close:
            log.close()
    else:
        print(output)

def resize(self):
    for source in self:
        write_log("Begin work on {}".format(source))
        sourceName = source[:-4]
        resized = "{}[576p].mkv".format(sourceName)
        if source[-6:] == "[576p]":
            rename(source, path.join(done, source))
        if path.isfile(resized):
            print("File {} exists already".format(resized))
            write_log("Resized version existed.")
        else:
            mp4 = sourceName + ".mp4"
            if name == 'nt':
                avs = sourceName + ".avs"
                tc = sourceName + ".txt"
                cache = sourceName + ".ffindex"
                avsfile = open(avs, "w")
                avsfile.write('FFMS2_FFVideoSource("{}",cachefile="{}",timecodes="{}",width=1024,height=576,resizer="LANCZOS")'.format(source, cache, tc))
                avsfile.close()
            system('{} {} --output "{}" "{}"'.format(x264, x264opts, mp4, avs))
            system('mkvmerge -o "{}" -D "{}" --timecodes "1:{}" "{}"'.format(resized, source, tc, mp4))
            write_log("Resize completed. Cleaning...")
            if removeTempFiles:
                for i in (mp4, tc, cache, avs):
                    remove(i)
            rename(resized, path.join(done, resized))
            write_log("Cleaning successful.")

dirList = glob.glob("*.[mMaA][kKpPvV][vV4iI]")

if dirList:
    write_log("Found:")
    for i in dirList:
        write_log("    {}".format(i))
    if not test:
        resize(dirList)
    write_log("Finished.",close=True)