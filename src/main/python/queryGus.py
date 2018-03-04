import os
import sys
import fileinput
import json
import gus
import sfdcid


def queryAndAssign(fileinfos, gusIdCache, sessionId):
    idsToRecordTypes = gus.query_gus(gusIdCache, sessionId)
    gus.assignRecordTypes(fileinfos, idsToRecordTypes)
    emitFileInfos(fileinfos)

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
    if (not gusId):
        # there's no work id, check for a task id
        taskId = sfdcid.to15(onefile['p4.gustaskid'])
        if (not taskId):
            sys.stderr.write("no well formed gus work item or task found: {0}, workid='{1}', taskid='{2}'\n".format(onefile['filename'], onefile['p4.gusid'], onefile['p4.gustaskid']))
        else:
            sys.stderr.write("TODO: retrieve gus work item from gus task id")
    else:
        if (not gusId in gusIdCache):
            if count >= maxQueryCount:
                queryAndAssign(fileinfos, gusIdCache, sessionId)

                # reset local caches
                fileinfos = []
                gusIdCache = set()
                count = 1
            else:
                count += 1
            gusIdCache.add(gusId)
        fileinfos.append(onefile)
if fileinfos:
    queryAndAssign(fileinfos, gusIdCache, sessionId)

