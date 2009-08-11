#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, zlib
#import subprocess
#import shutil
#from optparse import OptionParser

def crc32_checksum(filename):
    crc = 0
    p_reset = "\x08"*8
    file = open(filename, "rb")
    buff_size = 65536
    size = os.path.getsize(filename)
    done = 0
    try:
        while True:
            data = file.read(buff_size)
            done += buff_size
            sys.stdout.write("%7d"%(done*100/size) + "%" + p_reset)
            if not data:
                break
            crc = zlib.crc32(data, crc)
    except KeyboardInterrupt:
        sys.stdout.write(p_reset)
        file.close()
        sys.exit(1)
    sys.stdout.write(p_reset)
    file.close()
    if crc < 0:
        crc &= 2**32-1
    return "%.8X" %(crc)

if os.name == 'nt':
    zip = '"C:\\Program Files\\7-Zip\\7z.exe" a '
    xdelta = "D:\\xdelta3.exe"
    xdeltaexe = xdelta
elif os.name == 'posix':
    zip = 'zip -j '
    xdelta = 'xdelta3'
    xdeltaexe = '/home/ricardo/xdelta3.exe'


def proj():
    print '''Available projects:
        'fma' - Fullmetal Alchemist (2009)
        'chi' - Chi's Sweet Home
        'pack' - Raw to Final Pack
        '''
        
    project = raw_input("What's the project?: ")

    return project

if len(sys.argv) > 1:
    if sys.argv[1] == 'fma' or 'chi' or 'pack':
        project = sys.argv[1]
    else: project = proj()
else:
    project = proj()

if project == 'pack':
    print "rofl"
    if len(sys.argv) <= 3:
        print   '''Usage: pack <old file> <new file>
                This script calculates crc32, renames new file with it,
                patches with xdelta3, makes .bat file,
                and finally, packs everything in a .zip
                Example: pack "raw.avi" "final.mkv"'''
        exit()

    old = sys.argv[2]
    filename = sys.argv[3]
    ext = filename[-4:]
    filename = filename[:-4]

    print "\tChecksum... ",

    crc = crc32_checksum(filename + ext)

    print "\tdone."

    print "\tRenaming... ",


    nome  = filename + "_[" + str(crc) + "]" + ext
    zipfile = nome[:-4] + ".zip "
    nomebatch = nome[:-4] + ".bat"
    batfile = nomebatch
    batch = open(batfile, "w")
    lolo = ''
    rofl = []

    os.rename(filename + ext, nome)

    print "\tdone."

    print "\tPatch... "

    os.system(xdelta + " -e -9 -s \"" + old + "\" \"" + nome + "\" \"" + nome[:-4] + '.xdelta"')

    print "\tdone."

    patch = "xdelta3.exe -d " + nome[:-4] + ".xdelta"

    batch.write(patch)
    rofl.append(nome[:-4] + ".xdelta")
    lolo = lolo + "\"" + nome[:-4] + ".xdelta\" "
        
    batch.close()

    print "Packing... ",

    os.system(zip + zipfile + lolo + xdeltaexe + " " + batfile + "> " + os.devnull)

    print "\t\tdone."

    print "Cleaning up... ",

    for meh in rofl:
        os.remove(meh)
    os.remove(batfile)

# Needless
if project == 'needless':
    
    raw = sys.argv[2] or "raw.mkv"
    subs = sys.argv[3] or "final.ass"
    rawsource = raw_input("Who's the raw from? [default: Zero-Raws] ") or ''
    epno = os.path.basename(os.getcwd())
    title = raw_input("What's the name of the episode? ") or ''
    if title != '':
        if rawsource != '':
            rawsource = ' --track-name "1:[' + rawsource + '] Needless - ' + epno \
            + ': ' + title + '"'
        else:
            rawsource = ' --track-name "1:[Zero-Raws] Needless - ' + epno + '"'
        title = ' --title "[GarSubs] Needless - ' + epno + ': ' + title
        
    muxed = "[GarSubs]_Needless_-_" + epno + ".mkv"
    if os.path.isfile('chapters.xml'):
        chapters = ' --chapter-language "por" --chapters chapters.xml'
    else:
        chapters = ''
    fontlist = sys.argv[4:]# or os.listdir("../fonts/")
    fonts = ''
    for font in fontlist:
        fonts = fonts + ' --attachment-mime-type application/x-truetype-font' \
            + ' --attachment-name ' + font[9:] + ' --attach-file ' + font
    print "muxing... "
    comando = 'mkvmerge -o "' + muxed + '" --language "1:jpn"' + rawsource + \
        ' --default-track "1:yes" ' \
        '--language "2:jpn" --track-name "2:AAC 2.0" ' \
        '--default-track "2:yes" -a 2 -d 1 -S "' + raw + '" --language "0:por"' \
        ' --track-name "0:ASS com estilos" --default-track "0:yes" -s 0 -D' \
        ' -A "' + subs + '" --track-order "0:1,0:2,1:0" ' + fonts + title \
        + chapters
    print comando
    os.system(comando)
    print "checksumming... "
    crc = crc32_checksum(muxed)
    name = muxed[:-4] + '_[' + crc + ']'
    batfile = name + '.bat'
    zipfile = name + '.zip'
    deltafile = name + '.xdelta'
    epfile = name + '.mkv'
    batch = open(batfile, 'w')
    print "renaming... "
    os.rename(muxed, epfile)
    print "patching... "
    os.system(xdelta + ' -e -9 -s "' + raw + '" "' \
        + epfile + '" "' + deltafile + '"')
    print "writing batch..."
    batch.write ("xdelta3.exe -d " + deltafile + "\npause")
    batch.close()
    print "zipping... "
    os.system('%s"%s" "%s" "%s" "%s"> %s' % \
        (zip, zipfile, deltafile, xdeltaexe, batfile, os.devnull))
    print "cleaning up... "
    os.remove(deltafile)
    os.remove(batfile)
    print "done. Enjoy [GarSubs] Needless - " + epno + \
        ": " + title + "! CRC is: " + crc

# Saint Seiya
if project == 'ss':
    show = "Saint Seiya: The Lost Canvas"
    showfilename = "Saint_Seiya_The_Lost_Canvas"
    raw = sys.argv[2] or "raw.mkv"
    audio = sys.argv[3] or "audio.mp4"
    subs = sys.argv[4] or "final.ass"
    rawsource = raw_input("Who's the raw from? [default: Dm258.Raws] ") or ''
    epno = os.path.basename(os.getcwd())
    title = raw_input("What's the name of the episode? ") or ''
    if title != '':
        if rawsource != '':
            rawsource = ' --track-name "1:[' + rawsource + '] ' + show + ' - ' + epno \
            + ': ' + title + '"'
        else:
            rawsource = ' --track-name "1:[Dm258.Raws] ' + show + ' - ' + epno + '"'
        title = ' --title "[FDP] ' + show + ' - ' + epno + ': ' + title
        
    muxed = '[FDP]_' + showfilename + '_-_' + epno + '.mkv'
    if os.path.isfile('chapters.xml'):
        chapters = ' --chapter-language "por" --chapters chapters.xml'
    else:
        chapters = ''
    fontlist = sys.argv[5:]# or os.listdir("../fonts/")
    fonts = ''
    for font in fontlist:
        fonts = fonts + ' --attachment-mime-type application/x-truetype-font' \
            + ' --attachment-name ' + font[9:] + ' --attach-file ' + font
    print "muxing... "
    comando = 'mkvmerge -o "' + muxed + '" --language "1:jpn"' + rawsource + \
        ' --default-track "1:yes" ' \
        '--language "2:jpn" --track-name "2:LC-AAC 2.0" ' \
        '--default-track "2:yes" -a 2 -d 1 -S "' + raw + '" --language "0:por"' \
        ' --track-name "0:ASS com estilos" --default-track "0:yes" -s 0 -D' \
        ' -A "' + subs + '" --track-order "0:1,0:2,1:0" ' + fonts + title \
        + chapters
    print comando
    os.system(comando)
    print "checksumming... "
    crc = crc32_checksum(muxed)
    name = muxed[:-4] + '_[' + crc + ']'
    batfile = name + '.bat'
    zipfile = name + '.zip'
    deltafile = name + '.xdelta'
    epfile = name + '.mkv'
    batch = open(batfile, 'w')
    print "renaming... "
    os.rename(muxed, epfile)
    print "patching... "
    os.system(xdelta + ' -e -9 -s "' + raw + '" "' \
        + epfile + '" "' + deltafile + '"')
    print "writing batch..."
    batch.write ("xdelta3.exe -d " + deltafile + "\npause")
    batch.close()
    print "zipping... "
    os.system('%s"%s" "%s" "%s" "%s"> %s' % \
        (zip, zipfile, deltafile, xdeltaexe, batfile, os.devnull))
    print "cleaning up... "
    os.remove(deltafile)
    os.remove(batfile)
    print 'done. Enjoy [FDP] ' + show + ' - ' + epno + \
        ": " + title + "! CRC is: " + crc

# Fma
if project == 'fma':
    
    print   "Title ex: Laboratorio No. 5\n" \
            "Episode number ex: 08"
    raw = sys.argv[3] or "raw.mkv"
    subs = sys.argv[4] or "final.ass"
    rawsource = raw_input("Who's the raw from? [default: Raws-4U] ") or "Raws-4U"
    title = raw_input("What's the name of the episode? ")
    epno = os.path.basename(os.getcwd())
    muxed = "[FDP]_Fullmetal_Alchemist_(2009)_-_" + epno + ".mkv"
    if sys.argv[2] == 'final':
        chapters = ' --chapters chapters.pt.xml'
    else:
        chapters = ''
    fontlist = sys.argv[5:] or os.listdir("../fonts/")
    fonts = ''
    for font in fontlist:
        fonts = fonts + ' --attachment-mime-type application/x-truetype-font' \
            + ' --attachment-name ' + font[9:] + ' --attach-file ' + font
    print "muxing... "
    os.system('mkvmerge -o "' + muxed + '" --language "1:jpn" --track-name ' \
        '"1:[' + rawsource + '] Fullmetal Alchemist (2009) - ' + epno + \
        ': ' + title + '" --default-track "1:yes" --display-dimensions ' \
        '"1:1280x720" --language "2:jpn" --track-name "2:AAC 2.0" ' \
        '--default-track "2:yes" -a 2 -d 1 -S "' + raw + '" --language "0:por"' \
        ' --track-name "0:ASS com estilos" --default-track "0:yes" -s 0 -D' \
        ' -A "' + subs + '" --track-order "0:1,0:2,1:0" ' + fonts + ' --title ' \
        '"[FDP] Fullmetal Alchemist (2009) - ' + epno + ': ' + title + '" ' \
        '--chapter-language "por"' + chapters)
    print "checksumming... "
    crc = crc32_checksum(muxed)
    name = muxed[:-4] + '_[' + crc + ']'
    batfile = name + '.bat'
    zipfile = name + '.zip'
    deltafile = name + '.xdelta'
    epfile = name + '.mkv'
    batch = open(batfile, 'w')
    print "renaming... "
    os.rename(muxed, epfile)
    print "patching... "
    os.system(xdelta + ' -e -9 -s "' + raw + '" "' \
        + epfile + '" "' + deltafile + '"')
    print "writing batch..."
    batch.write ("xdelta3.exe -d " + deltafile + "\npause")
    batch.close()
    print "zipping... "
    os.system('%s"%s" "%s" "%s" "%s"> %s' % \
        (zip, zipfile, deltafile, xdeltaexe, batfile, os.devnull))
    print "cleaning up... "
    os.remove(deltafile)
    os.remove(batfile)
    print "done. Enjoy [FDP] Fullmetal Alchemist (2009) - " + epno + \
        ": " + title + "! CRC is: " + crc
#    arrumar = raw_input("Would you like to prep the ep for distro? (y/n): ")
#    if arrumar == 'y':
#        shutil.move(epfile, '../../../done/fma/' + epfile)
#        shutil.move(zipfile, '/home/ricardo/www/patches/fma/' + zipfile)
#        shutil.move(subs, '/home/ricardo/www/scripts/fma/' + name + '.ass')
        

# Chi
elif project == 'chi':
    min = input("First episode to mux: ")
    max = input("Last episode to mux: ")

    eps = range(min, max + 1)

    nomebatch = "patch%03d-%03d" % (min, max)
    batfile = nomebatch + ".bat"
    zipfile = nomebatch + ".zip "
    batch = open(batfile, "w")
    lolo = ''
    rofl = []
    fontlist = sys.argv[2:]
    fonts = ''
    for font in fontlist:
        fonts = fonts + ' --attachment-mime-type application/x-truetype-font' \
            + ' --attachment-name ' + font[9:] + ' --attach-file ' + font
    for count in eps:
        count2 = "%03d" % count
        count = str(count)
        print "Episodio %s:" % count
        print r"    Muxing... "
        os.system("mkvmerge -o " + count2 + '.mkv  --language 0:por --track-name "0:ASS com estilos" --default-track 0:yes --forced-track 0:no -s 0 -D -A "Epi ' + count + '.ass" --language 1:jpn --track-name "1:[FDP] Chi\'s Sweet Home - ' + count2 + '" --default-track 1:yes --forced-track 1:no --language 2:jpn --track-name "2:AAC 2.0" --default-track 2:yes --forced-track 2:no -a 2 -d 1 -S ' + count2 + '.mp4 --track-order "1:1,1:2,0:0" ' + fonts + ' --title "[FDP] Chi\'s Sweet Home - ' + count2 + '" --chapters chapter.xml')

        print "\tdone."
        
        print r"    Checksuming... "
        
        crc = crc32_checksum(count2 + ".mkv")
        
        print "\tdone."
        
        print r"    Renaming... "
        
        nome  = "[FDP]_Chi's_Sweet_Home_-_" + count2 + "_[" + str(crc) + "]."
        
        os.rename(count2 + ".mkv", nome + "mkv")
        
        print "\tdone."
        
        print r"    Patch... "
        
        os.system(xdelta + " -e -9 -s " + count2 + ".mp4 \"" + nome + "mkv\" \"" + nome + 'xdelta"')
        
        print "\tdone."
        
        patch = "xdelta3.exe -d " + nome + "xdelta"
        
        batch.write(patch + "\n")
        rofl.append("[FDP]_Chi's_Sweet_Home_-_" + count2 + "_[" + str(crc) + "].xdelta")
        lolo = lolo + "\"[FDP]_Chi's_Sweet_Home_-_" + count2 + "_[" + str(crc) + "].xdelta\" "
        
    batch.close()

    print r"Packing... "

    os.system(zip + zipfile + lolo + xdeltaexe + " " + batfile + "> " + os.devnull)

    print "\t\tdone."

    print r"Cleaning up... "

    for meh in rofl:
        os.remove(meh)
    os.remove(batfile)

    print "\tdone."
