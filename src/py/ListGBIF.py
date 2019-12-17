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

def getDataset():
    urlGBIF = 'http://api.gbif.org/v1/organization/1928bdf0-f5d2-11dc-8c12-b8a03c50a862/publishedDataset'

    out = open("output/GBIF8.csv", "a")

    check = []

    offset = 0
    limit = 10
    i = 1
    while True:
        urlComplete = urlGBIF+'?limit='+str(limit)+'&offset='+str(offset)
        print(urlComplete)
        response = requests.get(urlComplete)
        data = response.json()

        for r in data['results']:
            key = ""
            created = ""
            modified = ""
            recordCount = -1
            title = ""
            iptId = ""
            url = ""

            key = r['key']

            if (key in check):
                print("ERROR "+key)
                return

            check.append(key)

            print(str(i) + " / " +key)
            i = i + 1

            title = r['title']

            responseDetail = requests.get('http://api.gbif.org/v1/dataset/'+key)
            dataDetail = responseDetail.json()
            created = dataDetail['created']
            modified = dataDetail['modified']

            foundIdentifier = False
            for identifier in dataDetail['identifiers']:
                if (identifier['type'] == "URL"):
                    url = identifier['identifier']
                    foundIdentifier = True
                    break

            if (foundIdentifier == False):
                responseEndpoint = requests.get('http://api.gbif.org/v1/dataset/'+key+'/endpoint')
                dataEndpoint = responseEndpoint.json()
                for endpoint in dataEndpoint:
                    if ((endpoint['type'] == "DWC_ARCHIVE") or (endpoint['type'] == "EML")):
                        url = endpoint['url']
                        break

            responseCount = requests.get('http://api.gbif.org/v1/occurrence/count?datasetKey='+key)
            recordCount = responseCount.text

            iptId = url[(url.rfind('=')+1)::]
            out.write(key+";"+title+";"+created+";"+modified+";"+str(recordCount)+";"+iptId+";"+url+"\n")

        if data['endOfRecords']:
            break
        else:
            offset = offset + limit

    out.close()

def getFileDataset():
    dsList = [f for f in glob.glob("data/MAJ/*.zip")]
    dsNameList = []

    out = open("output/MAJ.csv", "a")

    for ds in dsList:
        # DIFFUSER=14 MAJ=9
        name = os.path.splitext(ds)[0][9::]
        print(name)
        archive = zipfile.ZipFile(ds, 'r')
        with archive.open('Occurence.txt') as f:
            line_count = 0
            for line in f:
                line_count += 1
        print(line_count)
        out.write(name+";"+str(line_count)+"\n")

    out.close()

def reconcil():

    out = open("output/GBIF8c.csv", "a")

    drDiffuser = {}
    with open("output/SAVE/DIFFUSER.csv", newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        csv_rows = list(csv_reader)

        for row in csv_rows:
            drDiffuser[row[0]] = row[1]

    drMaj = {}
    with open("output/SAVE/MAJ.csv", newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        csv_rows = list(csv_reader)

        for row in csv_rows:
            drMaj[row[0]] = row[1]

    drDiffuserFound = []
    drMajFound = []

    with open("output/GBIF8.csv", newline='') as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=';')
            csv_rows = list(csv_reader)

            for row in csv_rows:
                id = row[5]
                action = "NOT_FOUND"
                count = ""
                diff = ""
                if (id.startswith("IPT-")):
                    id = id[4::]
                    if (id in drDiffuser):
                        action = "DIFFUSER"
                        count = int(drDiffuser[id]) - 1
                        diff = int(count) - int(row[4])
                        drDiffuserFound.append(id)
                    if (id in drMaj):
                        action = "MAJ"
                        count = int(drMaj[id]) - 1
                        diff = int(count) - int(row[4])
                        drMajFound.append(id)

                out.write(row[0]+";"+row[1]+";"+row[2]+";"+row[3]+";"+row[4]+";"+row[5]+";"+row[6]+";"+action+";"+str(count)+";"+str(diff)+"\n")

            for id in drDiffuser:
                if (id not in drDiffuserFound):
                    count = int(drDiffuser[id]) - 1
                    out.write(";;;;;"+id+";;DIFFUSER;"+str(count)+";\n")

            for id in drMaj:
                if (id not in drMajFound):
                    count = int(drMaj[id]) - 1
                    out.write(";;;;;"+id+";;MAJ;"+str(count)+";\n")

    out.close()

def createSH():
    dsList = [f for f in glob.glob("/workspace/ipt-batch-import-inpn/results/DIFFUSER/*")]
    out = open("output/copyDIFFUSER.sh", "a")
    #MAJ 45 DIFFUSER 50
    for ds in dsList:
        name = os.path.splitext(ds)[0][50::]
        print(name)
        out.write("sudo rm -Rf /data/www/private/ipt/ipt_data_inpn/resources/"+name+" \n")
        out.write("sudo cp -R "+name+" /data/www/private/ipt/ipt_data_inpn/resources \n")
    out.close()
    dsList = [f for f in glob.glob("/workspace/ipt-batch-import-inpn/results/MAJ/*")]
    out = open("output/copyMAJ.sh", "a")
    #MAJ 45 DIFFUSER 50
    for ds in dsList:
        name = os.path.splitext(ds)[0][45::]
        print(name)
        out.write("sudo rm -Rf /data/www/private/ipt/ipt_data_inpn/resources/"+name+" \n")
        out.write("sudo cp -R "+name+" /data/www/private/ipt/ipt_data_inpn/resources \n")
    out.close()

def createPython():
    dsList = [f for f in glob.glob("/workspace/ipt-batch-import-inpn/results/DIFFUSER/*")]
    dsNameList = []

    out = open("output/pythonPublishDIFFUSER", "a")

    for ds in dsList:
        name = os.path.splitext(ds)[0][50::]
        print(name)
        out.write("time.sleep(0.1)\n")
        out.write("publish(\""+name+"\", session)\n")

    out.close()

    out = open("output/pythonRegisterDIFFUSER", "a")

    for ds in dsList:
        name = os.path.splitext(ds)[0][50::]
        print(name)
        out.write("time.sleep(0.1)\n")
        out.write("register(\""+name+"\", session)\n")

    out.close()

def createPython2():
    dsList = [f for f in glob.glob("/workspace/ipt-batch-import-inpn/results/MAJ/*")]
    dsNameList = []

    out = open("output/pythonCheckMAJ", "a")

    for ds in dsList:
        name = os.path.splitext(ds)[0][45::]
        print(name)
        out.write("checkDR(\""+name+"\", session)\n")

    out.close()

    out = open("output/pythonCheckMAJ", "a")

    for ds in dsList:
        name = os.path.splitext(ds)[0][45::]
        print(name)
        out.write("checkDR(\""+name+"\", session)\n")

    out.close()


def main():
    getDataset()
    reconcil()

if __name__ == "__main__":
    main()
