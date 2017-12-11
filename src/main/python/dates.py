import sys
import fileinput
import json
from dateutil import parser


def get_all_dates(filename):
    with open(filename) as json_data:
        allDates = json.load(json_data)
    # convert from strings to dates
    for (k,v) in allDates.items():
        allDates[k] = {k2: (lambda v2: parser.parse(v2).date())(v2) for k2,v2 in v.items()}
    return allDates

# dateDict is dateDict<String,Date>
# date is a String containing a date
# returns a dict<String,int>
def get_date_diffs(dateDict, date):
    d = parser.parse(date).date()
    return {"date." + k: (lambda v: (d - v).days)(v) for k, v in dateDict.items()}

