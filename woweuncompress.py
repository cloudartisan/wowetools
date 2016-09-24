#!/usr/bin/env python


import sys
import os
from glob import glob
from commands import getstatusoutput


COMPRESSION_MAP = {
    "rar": "unrar x -y '%s'",
}


def main():
    try:
        path = sys.argv[1]
    except IndexError:
        sys.stderr.write("Usage: %s <path>\n" % sys.argv[0])
        sys.exit(1)

    if not os.path.isdir(path):
        sys.stderr.write("Usage: %s <path>\n" % sys.argv[0])
        sys.exit(1)

    for compression_type, decompress_cmd in COMPRESSION_MAP.items():
        for compressed in glob("%s/*.%s" % (path, compression_type)):
            status, output = getstatusoutput(decompress_cmd % compressed)
            print output


if __name__ == "__main__":
    main()
