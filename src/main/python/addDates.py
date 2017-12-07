import sys
import fileinput
import json
from dateutil import parser
import dates


if (not len(sys.argv) == 2):
    sys.stderr.write("usage: python dates.py <release-number>\n")
    exit()

releaseNumber = sys.argv[1]
alldates = dates.get_all_dates('dates.json')
if (releaseNumber not in alldates):
    sys.stderr.write("realase '{0}' not found\n".format(releaseNumber))
    exit()

release = alldates[releaseNumber]
for line in fileinput.input(sys.argv[2:]):
    info = json.loads(line)
    diffs = dates.get_date_diffs(release, info['p4.date'])
    info.update(diffs)
    print(json.dumps(info, separators=(',', ':')))

