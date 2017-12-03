import sys
import json
import subprocess


def query_gus(gusIds, sessionId):
    url = "https://gus.my.salesforce.com/services/data/v20.0/query/?q=SELECT+Id,Type__c+FROM+ADM_Work__c+WHERE+Id+in+(\'" + "','".join(gusIds) + "\')"
    auth = "Authorization: Bearer " + sessionId
    #sys.stderr.write("querying gus\n")
    #sys.stderr.write("url: {0}".format(url))
    #sys.stderr.write("auth: {0}".format(auth))
    process = subprocess.run(["curl", url, "-H", auth], stdout=subprocess.PIPE)
    gusResponse = process.stdout.decode(encoding='UTF-8')
    gusJson = json.loads(gusResponse)
    sys.stderr.write(json.dumps(gusJson, indent=4, sort_keys=True))

    return queryToIds(gusJson)

def queryToIds(gusJson):
    idsToRecordTypes = {}
    for gusRecord in gusJson['records']:
        idsToRecordTypes[gusRecord['Id'][:15]] = gusRecord['Type__c']

    return idsToRecordTypes

def assignRecordTypes(fileinfos, idsToRecordTypes):
    sys.stderr.write("gusids: {0}".format(idsToRecordTypes))
    for fileinfo in fileinfos:
        if ('p4.gusid' in fileinfo):
            if (fileinfo['p4.gusid'] in idsToRecordTypes):
                if (idsToRecordTypes[fileinfo['p4.gusid'][:15]] != 'Integrate'):
                    fileinfo['gus.worktype'] = idsToRecordTypes[fileinfo['p4.gusid'][:15]]
                else:
                    sys.stderr.write("integration: skipping: {0}\n".format(fileinfo['filename']))
            else:
                sys.stderr.write("no gus record type: skipping: {0}\n".format(fileinfo['p4.gusid']))
        elif ('filename' in fileinfo):
            sys.stderr.write("no gusid: skipping: {0}\n".format(fileinfo['filename']))

