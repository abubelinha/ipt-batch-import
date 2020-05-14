import os
import glob
import logging
import datetime
#import yaml
import csv
import re
import numpy as np
import requests
import zipfile
import json

GBIF_FILE = "/workspace/ipt-batch-import-inpn/portail/gbif-2020-04-09b.csv"
COLLECTORY_FILE = "/workspace/ipt-batch-import-inpn/portail/collectory-2020-04-09b.csv"
OUTPUT_FILE = "/workspace/ipt-batch-import-inpn/portail/reconcil-2020-04-09b.csv"

def getDatasetGBIF():
    urlPublisher = "https://api.gbif.org/v1/organization?country=FR&limit=1000"

    response = requests.get(urlPublisher)
    data = response.json()

    ds = []

    for publisher in data['results']:
        key = publisher["key"]
        ds = ds + getDatasetByPublisherGBIF(key)
        print ("DS Count = "+str(len(ds)))

    out = open(GBIF_FILE, "a")

    for d in ds:
        out.write(d)
        out.write("\n")

    out.close()

def getDatasetCountURL():
    urlPublisher = "https://api.gbif.org/v1/organization?country=FR&limit=1000"

    response = requests.get(urlPublisher)
    data = response.json()

    i = 1
    startUrl = "https://www.gbif.org/occurrence/search?"
    url = ""

    for publisher in data['results']:
        key = publisher["key"]
        url = url + "publishing_org=" + key + "&"
        if (i % 20 == 0):
            print(startUrl+url)
            url = ""
        i = i +1

    print(startUrl+url)

def getDatasetByPublisherGBIF(key):
    print("Find datasets for "+key)

    urlGBIF = 'http://api.gbif.org/v1/organization/' + key + '/publishedDataset'

    ds = []

    offset = 0
    limit = 10
    i = 1
    while True:
        urlComplete = urlGBIF+'?limit='+str(limit)+'&offset='+str(offset)
        response = requests.get(urlComplete)
        data = response.json()

        for r in data['results']:
            uuid = r['key']
            print("Found uuid: "+uuid)
            ds.append(uuid)

        if data['endOfRecords']:
            break
        else:
            offset = offset + limit

    return ds

def reconcil():
    collectoryData = {}
    with open(COLLECTORY_FILE, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        csv_rows = list(csv_reader)[1:]

        for row in csv_rows:
            data = {}
            data['name'] = row[1]
            data['count'] = row[3]
            data['drid'] = row[0]
            data['dpid'] = row[4]
            data['dpname'] = row[5]
            data['dpgbifid'] = row[6]
            collectoryData[row[2]] = data

    out = open(OUTPUT_FILE, "a")
    out.write("Data resource GBIF ID;Data resource;UID;DR Count;GBIF Count;Difference;Status;Data provider UID;Data provider name;Data provider GBIF ID;\n")

    i = 0
    for key in collectoryData:
        colcount = collectoryData[key]['count']
        drid = collectoryData[key]['drid']
        name = collectoryData[key]['name']

        dpid = collectoryData[key]['dpid']
        dpname = collectoryData[key]['dpname']
        dpgbifid = collectoryData[key]['dpgbifid']

        if (colcount == ""):
            colcount = "-1"

        print(str(i) + " / " +key+ " = " + colcount + " ["+drid+"]")
        i = i + 1

        recordCount = getDatasetCount(key)

        diff = recordCount - int(colcount)
        status = (diff == 0)

        out.write(key+";"+name+";"+drid+";"+colcount+";"+str(recordCount)+";"+str(diff)+";"+str(status)+";"+dpid+";"+dpname+";"+dpgbifid+"\n")

    with open(GBIF_FILE, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        csv_rows = list(csv_reader)

        for row in csv_rows:
            key = row[0]
            if (key not in collectoryData):
                recordCount = getDatasetCount(key)
                out.write(key+";NOT FOUND DATASET;;;"+str(recordCount)+";;;;;\n")


    out.close()

def getDatasetCount(key):
    responseCount = requests.get('http://api.gbif.org/v1/occurrence/count?datasetKey='+key)
    return int(responseCount.text)

def main():
    getDatasetCountURL()
    #getDatasetGBIF()
    #reconcil()

if __name__ == "__main__":
    main()
