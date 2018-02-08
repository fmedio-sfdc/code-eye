import sys
import fileinput
import json
from dateutil import parser
import dates

alldates = dates.get_all_dates('dates.json')
alldates['main'] = dates.get_clo_list(alldates)

for line in fileinput.input():
    info = json.loads(line)
    filename = info['filename']
    release = filename.split("/")[1]
    date = info['p4.date']
    label, daysBefore = dates.daysBefore(date, alldates[release])
    info.update({'date.label':label, 'date.days':daysBefore})
    print(json.dumps(info, separators=(',', ':')))

