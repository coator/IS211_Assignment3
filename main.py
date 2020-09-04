import argparse
import urllib.request
import tempfile
import shutil
import csv
import re
from collections import Counter
import time



def urlparse():
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
    with open(urlfile, 'rt') as f:
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
    print(totalcount, pictcount)
    print("Image requests account for {0}% of all requests".format(float(totalcount / pictcount).__round__(2)))

def statBrowserUse(datafile):
    browserlist = []
    for item in datafile:
        test = item[2].split(' ')
        print(item[2])
        #TODO - work on regex string
        for x in ('Firefox', 'Chrome\/ \sSafari\/[0-9]*', 'Trident','Safari'):
            if re.search(x, item[2], re.IGNORECASE) is not None:
                browserlist.append(x)
                print(browserlist)
                break
            else:
                pass
    print(Counter(browserlist))


url = urlparse()
url = downloadData(url)
url = processData(url)
pictSearchPercent(url)
statBrowserUse(url)
