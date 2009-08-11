#!/usr/bin/python
# Filename: crc32.py

import sys, zlib

def crc32_checksum(filename):
    """Returns a CRC32 checksum.
    
    Accepts only files."""
    crc = 0
    file = open(filename, "rb")
    buff_size = 65536
    done = 0
    try:
        while True:
            data = file.read(buff_size)
            done += buff_size
            if not data:
                break
            crc = zlib.crc32(data, crc)
    except KeyboardInterrupt:
        file.close()
        sys.exit(1)

    file.close()
    if crc < 0:
        crc &= 2**32-1
    return "%.8X" %(crc)

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        for file in sys.argv[1:]:
            print "%s \t\t\t %s" % (file, crc32_checksum(file))