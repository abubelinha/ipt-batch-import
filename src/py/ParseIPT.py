import os
import glob
import logging
import datetime
#import yaml
import csv
import re
import requests
import zipfile
import time

IPT_URL = 'http://ipt-inpn.gbif.fr/'
IPT_USER = 'sylvain.morin@mnhn.fr'
IPT_PWD = ''

def login():
    session = requests.Session()
    session.post(IPT_URL)
    data = {"email": IPT_USER, "password": IPT_PWD, "csrfToken": session.cookies['CSRFtoken'], "portal.login": "login"}
    session.post(IPT_URL + 'login.do', data=data)
    return session

def loadData():
    session = login()
    responseCheck = session.get(IPT_URL + 'manage')
    text = responseCheck.text

    start = "var aDataSet = ["
    end = "];"
    startID = text.find(start)+len(start)
    endID = text.find(end, startID)

    data = "[" + text[startID:endID] + "]"

    return eval(data)

def check():
    data = loadData()

    print (data)

    out = open("output/IPT.csv", "a")
    out.write("ID;TITLE;COUNT;MODIFIED;PUBLICATION\n")

    for ds in data:
        status = ds[2]
        count = ds[5]
        modified = ds[6]
        publication = ds[7]

        count = str(count).replace(',', '')

        header = ds[1]
        title = header[header.find("<if>")+4:header.rfind("</a>")]
        url = header[header.find("href='")+6:header.rfind("'>")]
        id = url[(url.rfind('=')+1)::]

        if (status == "Not registered"):
            out.write(id+";"+title+";"+str(count)+";"+modified+";"+publication+";"+url+"\n")

    out.close()

def main():
    check()


if __name__ == "__main__":
    main()
