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

i = 0

DIFFUSERList = []
MAJList = []

def load(path, drList):
    dsList = [f for f in glob.glob(path+"*")]
    for ds in dsList:
        name = os.path.splitext(ds)[0][len(path)::]
        drList.append(name)

def loadDR():
    global DIFFUSERList
    load("/workspace/ipt-batch-import-inpn/results/DIFFUSER/", DIFFUSERList)
    global MAJList
    load("/workspace/ipt-batch-import-inpn/results/MAJ/", MAJList)

def executeAll():
    session = login()

def checkAll():
    session = login()
    out = open("output/resCheckMAJ", "a")
    for dr in MAJList:
        success = checkDR(dr, session)
        out.write(dr+" "+str(success)+"\n")
    out.close()
    out = open("output/resCheckDIFFUSER", "a")
    for dr in DIFFUSERList:
        success = checkDR(dr, session)
        out.write(dr+" "+str(success)+"\n")
    out.close()

def checkHardAll():
    session = login()
    out = open("output/resCheckHardMAJ", "a")
    for dr in MAJList:
        success = checkHardDR(dr, session)
        out.write(dr+" "+str(success)+"\n")
    out.close()
    out = open("output/resCheckHardDIFFUSER", "a")
    for dr in DIFFUSERList:
        success = checkHardDR(dr, session)
        out.write(dr+" "+str(success)+"\n")
    out.close()

def publishAll():
    session = login()
    for dr in MAJList:
        publish(dr, session)
    for dr in DIFFUSERList:
        publish(dr, session)

def checkDR(dr, session):
    responseCheck = session.get(IPT_URL + 'publicationlog.do?r='+dr)
    success = False
    if responseCheck.status_code == 200:
        if ("Archive version #1.1 generated successfully!" in responseCheck.text):
            success = True
    return success

def checkHardDR(dr, session):
    responseCheck = session.get(IPT_URL + 'manage/resource?r='+dr)
    success = False
    if responseCheck.status_code == 200:
        if ("<th>Version</th><td class=\"separator green\">1.1&nbsp;" in responseCheck.text):
            success = True
    return success

def login():
    session = requests.Session()
    session.post(IPT_URL)
    data = {"email": IPT_USER, "password": IPT_PWD, "csrfToken": session.cookies['CSRFtoken'], "portal.login": "login"}
    session.post(IPT_URL + 'login.do', data=data)
    return session

def publish(dr, session):
    print("Publish "+dr)
    data = {"r": dr, "currPubMode": "AUTO_PUBLISH_OFF", "publish": "Publish"}
    responsePublish = session.post(IPT_URL + 'manage/publish.do', data=data)
    if responsePublish.status_code == 200:
        while True:
            responseReport = session.get(IPT_URL + 'manage/report.do?r='+dr)
            if responseReport.status_code == 200:
                print ("waiting...")
                if ("<divclass=\"completed\">" in responseReport.text):
                    return
                time.sleep(0.5)
            else:
                return

def register(dr, session):
    print("Register "+dr)
    data = {"r": dr, "register": "Register"}
    responseRegister = session.post(IPT_URL + 'manage/resource-registerResource.do', data=data)
    print(responseRegister)




def main():
    checkAll()


if __name__ == "__main__":
    loadDR()
    main()
