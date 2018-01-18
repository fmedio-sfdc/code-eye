import sys
import json
import subprocess
import sfdcid


def query_gus(gusIds, sessionId):
    url = "https://gus.my.salesforce.com/services/data/v20.0/query/?q=SELECT+Id,Type__c+FROM+ADM_Work__c+WHERE+Id+in+(\'" + "','".join(gusIds) + "\')"
    auth = "Authorization: Bearer " + sessionId
    #sys.stderr.write("querying gus\n")
    #sys.stderr.write("url: {0}".format(url))
    #sys.stderr.write("auth: {0}".format(auth))
    process = subprocess.run(["curl", url, "-H", auth], stdout=subprocess.PIPE)
    gusResponse = process.stdout.decode(encoding='UTF-8')
    gusJson = json.loads(gusResponse)
    #sys.stderr.write("json: {0}".format(gusJson))
    if (isinstance(gusJson, list) and 'errorCode' in gusJson[0].keys()):
        raise ValueError(gusJson[0]['message'])

    return queryToIds(gusJson)

def queryToIds(gusJson):
    idsToRecordTypes = {}
    for gusRecord in gusJson['records']:
        idsToRecordTypes[sfdcid.to15(gusRecord['Id'])] = gusRecord['Type__c']

    return idsToRecordTypes

def assignRecordTypes(fileinfos, idsToRecordTypes):
    for fileinfo in fileinfos:
        if ('p4.gusid' in fileinfo):
            gusid = sfdcid.to15(fileinfo['p4.gusid'])
            if (gusid in idsToRecordTypes):
                if (idsToRecordTypes[gusid] != 'Integrate'):
                    fileinfo['gus.worktype'] = idsToRecordTypes[gusid]
                else:
                    sys.stderr.write("integration: skipping: {0}\n".format(fileinfo['filename']))
            else:
                sys.stderr.write("no gus record type: skipping: {0}\n".format(gusid))
        elif ('filename' in fileinfo):
            sys.stderr.write("no gusid: skipping: {0}\n".format(fileinfo['filename']))

