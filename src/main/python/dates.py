import sys
import fileinput
import json
from dateutil import parser
import operator


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


def get_clo_list(dateDict):
    return {"date.main." + k : v['clo'] for k,v in dateDict.items()}

# returns a duple ('datelabel', num-days-before-labled-date)
# dates is a dict with labels for keys and dates for values
def daysBefore(date, dates):
    d = parser.parse(date).date()
    # get a sorted list of duples representing the dict key,value pairs
    sortedDates = sorted(dates.items(), key=operator.itemgetter(1))
    for (key, value) in sortedDates:
        if d <= value:
            return (key, (d-value).days)
    # if date > R2, then default to days relative to R2
    last = sortedDates[-1]
    return (last[0], (d-last[1]).days)
