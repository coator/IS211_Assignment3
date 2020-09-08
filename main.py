import argparse
import urllib.request
import tempfile
import shutil
import csv
import re
from collections import Counter
import datetime


def urlParse():
    parser = argparse.ArgumentParser(description='pull information from a url')
    parser.add_argument('--url', help='type a url string that will bring you to a website')
    args = parser.parse_args()
    return args.url


def downloadData(url):
    with urllib.request.urlopen(url) as response:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(response, tmp_file)
    return tmp_file.name


def processData(urlfile):
    processfile = list()
    with open(urlfile) as f:
        reader = csv.reader(f)
        for row in reader:
            processfile.append(list(row))
    return processfile


def pictSearchPercent(datafile):
    pictcount, totalcount = 0, 0
    for item in datafile:
        totalcount += 1
        for x in ('jpg', 'png', 'gif'):
            if re.search(x, item[0], re.IGNORECASE) is not None:
                pictcount += 1
                break
            else:
                pass
    print("Image requests account for {:.0%} of all requests".format(float(pictcount / totalcount)))


def statBrowserUse(datafile):
    browserlist = list()
    for item in datafile:
        # The order of this tuple is important since Chrome UA includes safari, but not the other way around
        for x in ('Firefox', 'Chrome', 'MSIE', 'Safari'):
            if re.search(x, item[2], re.IGNORECASE) is not None:
                browserlist.append(x)
                break
            else:
                pass
    # I saved a variable because I couldn't think of a better way to share the value in a more readable format.
    print('The most common browser is {0} with a total of {1} hits'.format(Counter(browserlist).most_common(1)[0][0],
                                                                           Counter(browserlist).most_common(1)[0][1]))


# extra credit
def statByHours(datafile):
    hourlist = list()
    for x in datafile:
        h = datetime.datetime.fromisoformat(x[1])
        hourlist.append(h.strftime('%-H'))
    hourlist = sorted(Counter(hourlist).items())
    for x in range(0, 25):
        if x >= len(hourlist):
            print('Hour {0} has 0 hits'.format(x))
        else:
            if str(x) == hourlist[x][0]:
                print('Hour {0} has {1} hits'.format(x, hourlist[x][1]))
            else:
                pass


def main():
    url = urlParse()
    urldata = downloadData(url)
    csvdata = processData(urldata)
    pictSearchPercent(csvdata)
    statBrowserUse(csvdata)
    statByHours(csvdata)


main()
