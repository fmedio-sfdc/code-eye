import os
import sys
import fileinput
import json
import gus
import sfdcid


def emitFileInfos(fileinfos):
    for info in fileinfos:
        print(json.dumps(info, separators=(',', ':')))

sessionId = os.environ.get('GUS_SESSION_ID')
if (not sessionId):
    sys.stderr.write("Error: Expected environment variable: GUS_SESSION_ID\n")
    exit()
#sys.stderr.write("SessionId: {0}".format(sessionId))

maxQueryCount = 200
count = 0
gusIdCache = set()
fileinfos = []
for line in fileinput.input():
    onefile = json.loads(line)
    gusId = sfdcid.to15(onefile['p4.gusid'])
    if (gusId):
        if (not gusId in gusIdCache):
            if count >= maxQueryCount:
                idsToRecordTypes = gus.query_gus(gusIdCache, sessionId)
                gus.assignRecordTypes(fileinfos, idsToRecordTypes)
                emitFileInfos(fileinfos)

                # reset local caches
                fileinfos = []
                gusIdCache = set()
                count = 1
            else:
                count += 1
            gusIdCache.add(gusId)
        fileinfos.append(onefile)
    else:
        sys.stderr.write("malformed gus id: {0}, {1}\n".format(onefile['filename'], onefile['p4.gusid']))
if fileinfos:
    gus.query_gus(fileinfos, gusIdCache)

