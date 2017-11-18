import ast
from io import StringIO
import json
import subprocess

import sys
import os
import pickle
import re


def decrement_patch_version(filename):
    filelog = get_file_history(filename)
    #print("filelog = {0}".format(filelog))
    return parse_filelog(filelog)

def parse_filelog(filelog):
    buffer = StringIO(filelog)
    filename = buffer.readline()
    #print("filename: {0}".format(filename))
    result = parse_revision(buffer.readline())
    if (result['p4.action'] == 'integrate' or result['p4.action'] == 'import' or result['p4.action'] == 'branch' or result['p4.action'] == 'merge'):
        result['filename'] = extract_moved_from_path(buffer.readline())
    else:
        editRevision = buffer.readline()
        #print("edit revision: {0}".format(editRevision))
        result = parse_revision(editRevision)
        result['filename'] = "{0}#{1}".format(filename.strip("\n"), result['p4.version'])

    return result

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
def get_file_history(p4FileRev):
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
    return '... moved from' in filelogOutput or '... branch from' in filelogOutput or '... copy from' in filelogOutput

def extract_moved_from_path(filelogOutput):
    buffer = StringIO(filelogOutput)
    for line in buffer:
        if was_moved(line):
            pattern = re.compile('.*//app(.*)$')
            match = pattern.match(line)
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
            sys.stderr.write("using cached result from '{0}'\n".format(cachefile))
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
