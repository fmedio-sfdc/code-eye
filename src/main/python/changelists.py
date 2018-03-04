import re
import sys
import json
from pathlib import Path
import sfdcid

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

    # wcheung is the person who performs code line cutover. Skip all of those cls
    if "release" in committer or "wcheung" in committer:
        return {}

    rev = re.search('@rev ([\w.]+)@', clStr, re.IGNORECASE)
    if rev:
        reviewer = rev.group(1).lower()
    else:
        reviewer = 'none'
    gusId = ''
    gus = re.search('https://gus.my.salesforce.com/.*(a07[\w\d]+)', clStr)
    if not gus:
        gus = re.search('https://gus.lightning.force.com/.*(a07[\w\d]+)', clStr)
    taskId = ''
    if not gus:
        task = re.search('https://gus.my.salesforce.com/.*(a0m[\w\d]+)', clStr)
        if not task:
            task = re.search('https://gus.lightning.force.com/.*(a0m[\w\d]+)', clStr)
        if task:
            taskId = sfdcid.to15(task.group(1))
    if gus:
        gusId = sfdcid.to15(gus.group(1))
    javaFiles = re.findall('... (//.+java#[0-9]+)', clStr)
    return {"p4.change":change, "p4.committer":committer, "p4.reviewer":reviewer, "p4.date":date, "p4.time":time, "p4.gusid":gusId, "p4.gustaskid":taskId, "p4.filecount":len(javaFiles)}

def parseFiles(clStr):
    info = parseInfo(clStr)
    if (not info):
        # empty means this CL was skipped for some reason
        return []
    elif (('p4.gusid' not in info or not info['p4.gusid']) and ('p4.gustaskid' not in info or not info['p4.gustaskid'])):
        sys.stderr.write("Skipping CL {0}. No gus work item or task found.\n".format(info['p4.change']))
        return []
    files = []
    javaFiles = re.finditer('... (//.+java#[0-9]+) ([\w\/]*)', clStr)
    for match in javaFiles:
        f = {'filename':match.group(1), 'p4.action':match.group(2)}
        f.update(info)
        files.append(f)
    return files

def peel_all(fname):
    f=open(fname,'r')
    while True:
        cl = peel(f)
        if (not cl):
            break
    f.close()


