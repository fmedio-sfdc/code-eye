import p4cache
import re
import sys
from pathlib import Path
import random
import json
import fileinput
import changelists


patchVersions = set()
# the following will iterate over all lines of all filenames on the cmd line OR stdin
# to use this script make sure all inputs with gus.worktype of type bug or test failure are provided
# before inputs with non-bug worktypes. You can either specify a file containing all bugs followed by a file
# containing no bugs, or simply provide stdin input that follows that is sorted bugs first
regex = re.compile('\.java#(\d+)')
nonBug = []
for line in fileinput.input():
    fixInfo = json.loads(line)
    fileRev = fixInfo['filename']
    if ('gus.worktype' in fixInfo and fixInfo['gus.worktype'] in ['Bug','Test Failure']):
        try:
            bugInfo = p4cache.decrement_patch_version(fileRev)
        except ValueError:
            sys.stderr.write("Skipping {0}, couldn't find decremented patch version\n".format(fileRev))
            continue

        if (not bugInfo):
            sys.stderr.write("Skipping {0}, previous version not found\n".format(fileRev))
            continue

        fileVersion = bugInfo["filename"]

        if (not fileVersion):
            sys.stderr.write("Skipping {0}, decremented version was null\n".format(fileRev))
            continue

        # copy bug file info to a new set of keys
        fixInfo['fix.filename'] = fileRev
        fixInfo['fix.p4.gusid'] = fixInfo['p4.gusid']
        fixInfo['fix.gus.worktype'] = fixInfo['gus.worktype']
        fixInfo['fix.p4.change'] = fixInfo['p4.change']

        # retrieve additional p4 info from previous change list, like filecount and reviewer
        bugCl = p4cache.get_cl(bugInfo['p4.change'])
        additionalBugInfo = changelists.parseInfo(bugCl)

        # replace previous p4 values with the values from the decremented CL
        fixInfo.update(bugInfo)
        fixInfo['filename'] = p4cache.p4GetCachedPath(fileVersion)
        patchVersions.add(fileVersion)

        fixInfo.update(additionalBugInfo)

        fixInfo["label"] = "1"
        print(json.dumps(fixInfo, separators=(',', ':')))
    else:
        nonBug.append(fixInfo)

for fixInfo in nonBug:
    fileRev = fixInfo['filename']
    if ('gus.worktype' in fixInfo
            and fileRev not in patchVersions):
        if (random.randrange(3) == 0): # only use 1/3 of the input files
            fixInfo["filename"] = p4cache.p4GetCachedPath(fileRev)
            fixInfo["label"] = "0"
            versionMatch = regex.search(fileRev)
            fixInfo["p4version"] = versionMatch.group(1)
            print(json.dumps(fixInfo, separators=(',', ':')))
#print(patchVersions)
