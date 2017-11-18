import re
import sys
import json
from pathlib import Path

def flush(fptr):
     last_pos = fptr.tell()
     line = fptr.readline()
     while line != '':
         if re.search('^Change', line):
             fptr.seek(last_pos)
             break
         last_pos = fptr.tell()
         line = fptr.readline()

def peel(fptr):
    flush(fptr)

    cl = fptr.readline()
    last_pos = fptr.tell()
    line = fptr.readline()
    while line != '':
        if re.search('^Change', line):
            fptr.seek(last_pos)
            return cl
        cl += line
        last_pos = fptr.tell()
        line = fptr.readline()
    return cl

def parseInfo(clStr):
    matched = re.search('Change (\d+) by ([\w.-]+)@[-:.\w\d]+ on (\d{4}/\d{2}/\d{2}) (\d{2}:\d{2}:\d{2})', clStr)
    if (not matched):
        sys.stderr.write("change not found for {0}\n".format(clStr))
        return {}
    change = matched.group(1)
    committer = matched.group(2)
    date = matched.group(3)
    time = matched.group(4)

    if "release" in committer:
        return {}

    rev = re.search('@rev ([\w.]+)@', clStr, re.IGNORECASE)
    if rev:
        reviewer = rev.group(1)
    gus = re.search('https://gus.my.salesforce.com/.*(a07[\w\d]+)', clStr)
    if not gus:
        gus = re.search('https://gus.lightning.force.com/.*(a07[\w\d]+)', clStr)
    if gus:
        gusId = gus.group(1)
    else:
        gusId = ''
    javaFiles = [f.group(1) for f in re.finditer('... (//.+java#[0-9]+)', clStr)]
    return {"p4.change":change, "p4.committer":committer, "p4.date":date, "p4.time":time, "p4.gusid":gusId, "p4.filecount":len(javaFiles)}

def parseFiles(clStr):
    info = parseInfo(clStr)
    if (not info):
        return []
    files = []
    javaFiles = [f.group(1) for f in re.finditer('... (//.+java#[0-9]+)', clStr)]
    for eachFile in javaFiles:
        fileDict = {"filename":eachFile}
        fileDict.update(info)
        files.append(fileDict)
    return files

def peel_all(fname):
    f=open(fname,'r')
    while True:
        cl = peel(f)
        if (not cl):
            break
    f.close()


