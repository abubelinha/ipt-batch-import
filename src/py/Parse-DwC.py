import os
import glob
import logging
import datetime
import csv
import re
import requests
import zipfile
import time

DWC_PATH                = "/workspace/ipt-batch-import-inpn/data/MANUAL"
RESULT_FILE_PATH        = "output/MAJ.csv"
OCCURRENCE_FILE_NAME    = "Occurence.txt"
CSV_SEPARATOR           = ";"

def printNameList():
    print(generateNameList())

def generateNameList():
    dwcList = []
    path = __getPath()

    fileList = [f for f in glob.glob(path+"*.zip")]
    for f in fileList:
        name = __extractName(f, path)
        dwcList.append(name)

    return dwcList

def generateNameReport():
    out = open(RESULT_FILE_PATH, "w")
    path = __getPath()

    fileList = [f for f in glob.glob(path+"*.zip")]
    for f in fileList:
        print("Parsing: "+f)
        name = __extractName(f, path)
        print("DwC Name: "+name)
        out.write(name+"\n")

    out.close()

def generateOccurrenceCountReport():
    out = open(RESULT_FILE_PATH, "w")
    path = __getPath()

    fileList = [f for f in glob.glob(path+"*.zip")]
    for f in fileList:
        print("Parsing: "+f)
        name = __extractName(f, path)
        print("DwC Name: "+name)
        archive = zipfile.ZipFile(f, 'r')
        with archive.open(OCCURRENCE_FILE_NAME) as arch:
            line_count = 0
            for line in arch:
                line_count += 1
        print("Occurrence count: "+str(line_count))
        out.write(name+CSV_SEPARATOR+str(line_count)+"\n")

    out.close()

def __getPath():
    return DWC_PATH if DWC_PATH.endswith("/") else DWC_PATH+"/"

def __extractName(f, path):
    return os.path.splitext(f)[0][len(path)::]

if __name__ == "__main__":
    printNameList()
