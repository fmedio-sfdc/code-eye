import os
import sys
import fileinput
from pathlib import Path
import json
import subprocess


def query_gus(fileinfos, gusIds):
    url = "https://gus.my.salesforce.com/services/data/v20.0/query/?q=SELECT+Id,Type__c+FROM+ADM_Work__c+WHERE+Id+in+(\'" + "','".join(gusIds) + "\')"
    auth = "Authorization: Bearer " + sessionId
    sys.stderr.write("querying gus\n")
    #sys.stderr.write("url: {0}".format(url))
    #sys.stderr.write("auth: {0}".format(auth))
    process = subprocess.run(["curl", url, "-H", auth], stdout=subprocess.PIPE)
    gusResponse = process.stdout.decode(encoding='UTF-8')
    gusJson = json.loads(gusResponse)
    #sys.stderr.write(json.dumps(gusJson, indent=4, sort_keys=True))

    #add work type to fileinfo
    types = {}
    for gusRecord in gusJson['records']:
        types[gusRecord['Id'][:15]] = gusRecord['Type__c']

    #sys.stderr.write(json.dumps(types))
    for fileinfo in fileinfos:
        if (fileinfo['p4.gusid']):
            fileinfo['gus.worktype'] = types[fileinfo['p4.gusid'][:15]]
            print(json.dumps(fileinfo, separators=(',', ':')))
        elif (fileinfo['filename']):
            sys.stderr.write("no gusid: skipping: {0}\n".format(fileinfo['filename']))

sessionId = os.environ.get('GUS_SESSION_ID')
if (not sessionId):
    sys.stderr.write("Error: Expected environment variable: GUS_SESSION_ID\n")
    exit()
#sys.stderr.write("SessionId: {0}".format(sessionId))

maxGusIds = 200
count = 0
gusIds = set()
fileinfos = []
for line in fileinput.input():
    onefile = json.loads(line)
    if (not onefile['p4.gusid'] in gusIds):
        if count >= maxGusIds:
            query_gus(fileinfos, gusIds)
            # initialize fileinfos to contain the one unprocessed file
            fileinfos = []
            gusIds = set()
            gusIds.add(onefile['p4.gusid'])
            count = 1
        else:
            gusIds.add(onefile['p4.gusid'])
            count += 1
    fileinfos.append(onefile)
if fileinfos:
    query_gus(fileinfos, gusIds)

