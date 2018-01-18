import ast
from io import StringIO
import json
import subprocess

import sys
import os
import pickle
import re


def decrement_patch_version(filename):
    filelog = getFilelog(filename)
    #print("filelog = {0}".format(filelog))
    return parse_filelog(filelog)

# expecting filelog output matching
# //app/206/patch/core/search/java/src/search/solr/client/impl/SolrServerImpl.java
#... #7 change 12898330 integrate on 2017/01/26 10:53:43 by autointeg@gridmanager:vm:10.252.14.128 (text) 'Autointegrate Change: [12897602'
#... ... copy from //app/206/freeze/core/search/java/src/search/solr/client/impl/SolrServerImpl.java#7
#... #6 change 12743941 edit on 2016/12/21 09:34:19 by guillaume.kempf@gridmanager:vm:10.252.15.5 (text) 'Entity Prediction: use speciali'
# for integrations there is a second line showing the origin of the integration
# for edits there is no second line
# in both cases we want to find the file and the CL that was the source of the previous revision
# if file was integrated then we need to find the change associated with the integration


# for any integration we will need to recursively call p4 filelog on the moved from version
# for example the version 4 of this file
# stager-ltm3:~ stager$ p4 filelog -m 2 -t "//app/208/patch/core/s2x/test/unit/java/src/strictunit/sync/s2x/sfdcchanges/S2XDeleteTest.java#4"
# returns output like this
#//app/208/patch/core/s2x/test/unit/java/src/strictunit/sync/s2x/sfdcchanges/S2XDeleteTest.java
#... #4 change 13472293 edit on 2017/04/20 12:26:16 by cschenkeltherolf@gridmanager:vm:10.252.13.193 (text) 'Only toggle S2XOrgCanSchedExter'
#... ... copy into //app/208/freeze/core/s2x/test/unit/java/src/strictunit/sync/s2x/sfdcchanges/S2XDeleteTest.java#4
#... ... copy into //app/main/core/s2x/test/unit/java/src/strictunit/sync/s2x/sfdcchanges/S2XDeleteTest.java#6
#... #3 change 13203123 integrate on 2017/03/17 09:26:06 by wcheung@wcheung-ltm (text) 'Autointegrate Control: @skip@ b'
#... ... copy into //app/208/freeze/core/s2x/test/unit/java/src/strictunit/sync/s2x/sfdcchanges/S2XDeleteTest.java#3
#... ... copy from //app/main/core/s2x/test/unit/java/src/strictunit/sync/s2x/sfdcchanges/S2XDeleteTest.java#5
# which means we need to find the CL that main#5 was checked in with:
#stager-ltm3:~ stager$ p4 filelog -m 1 -t  "//app/main/core/s2x/test/unit/java/src/strictunit/sync/s2x/sfdcchanges/S2XDeleteTest.java#5"
#//app/main/core/s2x/test/unit/java/src/strictunit/sync/s2x/sfdcchanges/S2XDeleteTest.java
#... #5 change 13200619 edit on 2017/03/16 18:39:05 by cschenkeltherolf@gridmanager:vm:10.252.19.143 (text) 'Test sync.s2x.sfdcchanges.S2XDe'
#... ... copy into //app/208/patch/core/s2x/test/unit/java/src/strictunit/sync/s2x/sfdcchanges/S2XDeleteTest.java#3
#... ... copy into //build/env/mirror/app/main/core/s2x/test/unit/java/src/strictunit/sync/s2x/sfdcchanges/S2XDeleteTest.java#4

def parse_filelog(filelog):
    buffer = StringIO(filelog)
    filename = buffer.readline()
    # skip the current revision
    line = buffer.readline()
    ignore = parse_revision(line)
    if (isIntegrate(ignore)):
        sys.stderr.write("ignoring integration cl:\n  {0}\n".format(line))
        buffer.readline() # ignore the next line too

    # parse the previous revision
    result = parse_revision(buffer.readline())
    if (isIntegrate(result)):
        integFile = buffer.readline()
        while (isIntegrate(result)):
            #sys.stderr.write("extracting\n {0}\n".format(integFile))
            integrateRev = extract_moved_from_path(integFile)
            if (not integrateRev):
                raise ValueError("couldn't extract move path from {0}\n".format(integFile))
            #sys.stderr.write("integrateRev\n {0}\n".format(integrateRev))
            integFilelog = getFilelog(integrateRev)
            #sys.stderr.write("filelog\n {0}\n".format(integFilelog))
            buffer2 = StringIO(integFilelog)
            filename = buffer2.readline()
            #sys.stderr.write("filename\n {0}\n".format(filename))
            nextLine = buffer2.readline()
            result = parse_revision(nextLine)
            #sys.stderr.write("revision\n {0}\n".format(nextLine))
            integFile = buffer2.readline()
    result['filename'] = "{0}#{1}".format(filename.strip("\n"), result['p4.version'])

    return result

integration_types = ['integrate', 'import', 'branch', 'merge', 'move/add']
def isIntegrate(revision):
    return revision['p4.action'] in integration_types

def parse_revision(filelogRevision):
        # grab the p4 info from the CL associated with the previous version of the file
        # from the p4 filelog documentation:
        # ... #rev change chnum action on date by user@client (type) 'description'

        change = re.search('... #(\d+) change (\d+) ([\w/]+) on (\d{4}/\d{2}/\d{2}) (\d{2}:\d{2}:\d{2}) by ([\w.-]+)@[-:.\w\d]+', filelogRevision)
        if (not change):
            raise ValueError("Error: could not parse p4 revision from input \n\t'{0}'\n".format(filelogRevision))

        result = {}
        result['p4.version'] = change.group(1)
        result['p4.change'] = change.group(2)
        result['p4.action'] = change.group(3)
        result['p4.date'] = change.group(4)
        result['p4.time'] = change.group(5)
        result['p4.committer'] = change.group(6)
        return result


# avoid calling this function for 'add' files. Only call it for 'edit' files
def getFilelog(p4FileRev):
    # p4 filelog -m 1 filename
    # -s = summary, i.e. ignoring non-contributory integrations
    # -t = time of day
    process = subprocess.run(["p4", "filelog", "-s", "-t", "-m", "2", p4FileRev], stdout=subprocess.PIPE)
    return process.stdout.decode(encoding='UTF-8')

def get_cl(changeId):
    # p4 describe -s changeId
    # -s = summary, i.e. ignoring line change details
    process = subprocess.run(["p4", "describe", "-s", changeId], stdout=subprocess.PIPE)
    return process.stdout.decode(encoding='UTF-8')

# expecting a line like this:
# ... ... moved from //app/main/core/sfdc/java/src/common/udd/BitsToEnableInPreWindow.java#1,#799
def was_moved(filelogOutput):
    return '... moved from' in filelogOutput or '... branch from' in filelogOutput or '... copy from' in filelogOutput or '... merge from' in filelogOutput or '... edit from' in filelogOutput

def extract_moved_from_path(filelogOutput):
    buffer = StringIO(filelogOutput)
    for line in buffer:
        if was_moved(line):
            pattern = re.compile('.*//app(.*)$')
            match = pattern.match(line)
            if (not match):
                return None
            path = "//app{0}".format(match.group(1))
            return re.sub(r'(\#\d+,)','',path)

patchExpr = re.compile(r'//app/\d+/.*')
def is_patch_path(filename):
    return patchExpr.match(filename) is not None


def p4cache(fn):
    def wrapper(*args, **kwargs):   # define a wrapper that will finally call "fn"    with all arguments
        if (len(args) != 1):
            raise ValueError('Expected exactly one paramter, which should be a P4 path')

        if (isP4Path(args[0])):
            path = args[0][2:]
            (head, tail) = os.path.split(path)
            cachefiletail = get_valid_filename(tail)
            cachefile = os.path.join(head, cachefiletail)

            # if cache exists -> load it and return its content
            if os.path.exists(cachefile):
                with open(cachefile, 'rb') as cachehandle:
                    #sys.stderr.write("using cached result from '{0}'\n".format(cachefile))
                    return pickle.load(cachehandle)

            res = fn(*args, **kwargs)

            os.makedirs(head, exist_ok=True)
            with open(cachefile, 'wb') as cachehandle:
                #sys.stderr.write("saving result to cache '{0}'\n".format(cachefile))
                pickle.dump(res, cachehandle)
        else:

            res = fn(*args, **kwargs)
        return res
    return wrapper

def isP4Path(path):
    return path.startswith('//')

@p4cache
def p4print(p4Path):
    if isP4Path(p4Path):
        print("p4print called with path {0}".format(p4Path))
        process = subprocess.run(["p4", "print", p4Path], stdout=subprocess.PIPE)
        return process.stdout
    else:
        output = subprocess.check_output(["cat",p4Path])
    return output

def p4GetCachedPath(p4Path):
    if (isP4Path(p4Path)):
        path = p4Path[2:]
        (head, tail) = os.path.split(path)
        cachefiletail = get_valid_filename(tail)
        cachefile = os.path.join(head, cachefiletail)

        # if cache exists -> load it and return its content
        if os.path.exists(cachefile):
            #sys.stderr.write("using cached result from '{0}'\n".format(cachefile))
            return cachefile

        process = subprocess.run(["p4", "print", "-q", p4Path], stdout=subprocess.PIPE)

        os.makedirs(head, exist_ok=True)
        with open(cachefile, 'wb') as cachehandle:
            sys.stderr.write("saving result to cache '{0}'\n".format(cachefile))
            cachehandle.write(process.stdout)
        return cachefile
    else:
        return p4Path


def get_valid_filename(s):
    """
    Stolen from https://github.com/django/django/blob/master/django/utils/text.py
    Return the given string converted to a string that can be used for a clean
    filename. Remove leading and trailing spaces; convert other spaces to
    underscores; and remove anything that is not an alphanumeric, dash,
    underscore, or dot.
    >>> get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)
