import re
import sys
import json
import changelists
from pathlib import Path

def flush_cl(fptr):
    last_pos = fptr.tell()
    line = fptr.readline()
    while line != '':
        if re.search('^Change', line):
            fptr.seek(last_pos)
            break
        last_pos = fptr.tell()
        line = fptr.readline()

def get_files_from_changelist(fname):
    f=open(fname,'r')
    allfiles = []
    while True:
        cl = changelists.peel(f)
        if (cl == ''):
            break
        # always skip autointegrations. They will be processed in the original p4 checkin
        if re.search('autointeg@', line):
            continue
        files = changelists.parseFiles(cl)
        allfiles.append(files)

    f.close()
    return allfiles


if (not len(sys.argv) == 2):
    sys.stderr.write("usage: python retrieve.py cls.txt\n")
    exit()
clFile = Path(sys.argv[1])
if (not clFile.is_file()):
    sys.stderr.write("changelist file not found: {0}\n".format(sys.argv[1]))
    exit()

cls = get_files_from_changelist(clFile)
for cl in cls:
    for fileinfo in cl:
        print(json.dumps(fileinfo, separators=(',', ':')))

