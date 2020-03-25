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

def loadDRfromList():
    global DIFFUSERList
    DIFFUSERList.append("IPT-4A9DDA1F-B719-3E13-E053-2614A8C02B7C")
    DIFFUSERList.append("IPT-4A9DDA1F-B723-3E13-E053-2614A8C02B7C")
    DIFFUSERList.append("IPT-4A9DDA1F-B724-3E13-E053-2614A8C02B7C")
    DIFFUSERList.append("IPT-4A9DDA1F-B770-3E13-E053-2614A8C02B7C")
    DIFFUSERList.append("IPT-4A9DDA1F-B7E1-3E13-E053-2614A8C02B7C")
    DIFFUSERList.append("IPT-4A9DDA1F-B913-3E13-E053-2614A8C02B7C")
    DIFFUSERList.append("IPT-4B288174-EF81-4338-E053-2614A8C07BAF")
    DIFFUSERList.append("IPT-5261A16F-5269-317C-E053-2614A8C0DE63")
    DIFFUSERList.append("IPT-56396C41-A819-0BAF-E053-2614A8C009A7")
    DIFFUSERList.append("IPT-5976981F-4247-0823-E053-2614A8C090A2")
    DIFFUSERList.append("IPT-5976981F-4256-0823-E053-2614A8C090A2")
    DIFFUSERList.append("IPT-5976981F-4257-0823-E053-2614A8C090A2")
    DIFFUSERList.append("IPT-6026F6D4-C00F-03FC-E053-2614A8C051EE")
    DIFFUSERList.append("IPT-60EDDD62-06F7-34F2-E053-2614A8C069FC")
    DIFFUSERList.append("IPT-6B55B62E-6E0A-312B-E053-2614A8C057A8")
    DIFFUSERList.append("IPT-7157800F-5164-2C0B-E053-2614A8C02328")
    DIFFUSERList.append("IPT-72481C94-1CCB-0314-E053-2614A8C0DD4B")
    DIFFUSERList.append("IPT-738E5E8A-C0DE-0741-E053-2614A8C0CFD1")
    DIFFUSERList.append("IPT-74034A9C-16F6-074A-E053-2614A8C024AF")
    DIFFUSERList.append("IPT-74A83318-A2C0-5074-E053-2614A8C0FC0D")
    DIFFUSERList.append("IPT-75444185-2A1C-4086-E053-2614A8C05C76")
    DIFFUSERList.append("IPT-76626686-1641-7E75-E053-2614A8C0BD30")
    DIFFUSERList.append("IPT-76EFAEAB-7FA3-70A1-E053-2614A8C07E17")
    DIFFUSERList.append("IPT-77F13CDC-A692-1182-E053-2614A8C078D6")
    DIFFUSERList.append("IPT-7A154045-B511-100A-E053-2614A8C010F0")
    DIFFUSERList.append("IPT-7A25EF24-8EA0-3A60-E053-2614A8C03E1D")
    DIFFUSERList.append("IPT-7A25EF24-8EA1-3A60-E053-2614A8C03E1D")
    DIFFUSERList.append("IPT-7A9FD8B0-067F-3D08-E053-2614A8C008A4")
    DIFFUSERList.append("IPT-7A9FD8B0-0680-3D08-E053-2614A8C008A4")
    DIFFUSERList.append("IPT-7CD4D1CC-7F72-23DA-E053-2614A8C0C0E7")
    DIFFUSERList.append("IPT-7E8C0240-FDA9-23D5-E053-2614A8C01CF5")
    DIFFUSERList.append("IPT-7FE7EEA1-4FF0-2E59-E053-2614A8C0E4CF")
    DIFFUSERList.append("IPT-7FFA942F-B5D0-2F1E-E053-2614A8C06DEC")
    DIFFUSERList.append("IPT-7FFA942F-B5DA-2F1E-E053-2614A8C06DEC")
    DIFFUSERList.append("IPT-7FFA942F-B5E2-2F1E-E053-2614A8C06DEC")
    DIFFUSERList.append("IPT-7FFA942F-B5EE-2F1E-E053-2614A8C06DEC")
    DIFFUSERList.append("IPT-7FFA942F-B5FC-2F1E-E053-2614A8C06DEC")
    DIFFUSERList.append("IPT-7FFA942F-B600-2F1E-E053-2614A8C06DEC")
    DIFFUSERList.append("IPT-7FFA942F-B60A-2F1E-E053-2614A8C06DEC")
    DIFFUSERList.append("IPT-7FFA942F-B644-2F1E-E053-2614A8C06DEC")
    DIFFUSERList.append("IPT-80BFC5CD-5762-4F39-E053-2614A8C0499E")
    DIFFUSERList.append("IPT-80BFF849-2F14-4F3B-E053-2614A8C0E4BD")
    DIFFUSERList.append("IPT-8277227F-2782-1CB8-E053-2614A8C0A95C")
    DIFFUSERList.append("IPT-8277A7B4-60DC-1CB6-E053-2614A8C078A8")
    DIFFUSERList.append("IPT-82CEA00C-F6EB-6837-E053-2614A8C0C1C0")
    DIFFUSERList.append("IPT-82CF8C15-9605-0311-E053-2614A8C04B78")
    DIFFUSERList.append("IPT-82EF6EE5-57CA-07C1-E053-2614A8C09B2B")
    DIFFUSERList.append("IPT-835A0784-3CC9-5C6C-E053-2614A8C0E687")
    DIFFUSERList.append("IPT-840AA080-E340-5A4A-E053-2614A8C0A391")
    DIFFUSERList.append("IPT-841C17C9-7CA0-6383-E053-2614A8C0E9B7")
    DIFFUSERList.append("IPT-845A8B5C-FA09-50BA-E053-2614A8C07C38")
    DIFFUSERList.append("IPT-845A8B5C-FA62-50BA-E053-2614A8C07C38")
    DIFFUSERList.append("IPT-845A8B5C-FA63-50BA-E053-2614A8C07C38")
    DIFFUSERList.append("IPT-845A8B5C-FA64-50BA-E053-2614A8C07C38")
    DIFFUSERList.append("IPT-845AC32D-06E2-50BC-E053-2614A8C08E54")
    DIFFUSERList.append("IPT-84620625-2FCA-0345-E053-2614A8C057EA")
    DIFFUSERList.append("IPT-84620625-2FCB-0345-E053-2614A8C057EA")
    DIFFUSERList.append("IPT-848464A4-798A-714B-E053-2614A8C01C91")
    DIFFUSERList.append("IPT-848464A4-798B-714B-E053-2614A8C01C91")
    DIFFUSERList.append("IPT-8514C47D-BFC5-7B29-E053-2614A8C02FEF")
    DIFFUSERList.append("IPT-8587C542-1FC6-03E3-E053-2614A8C07788")
    DIFFUSERList.append("IPT-862FB4BC-E5A5-54DC-E053-5014A8C02001")
    DIFFUSERList.append("IPT-86A0ADA6-CEF5-69DB-E053-5014A8C08810")
    DIFFUSERList.append("IPT-86DD4272-B01C-417D-E053-5014A8C0F6F8")
    DIFFUSERList.append("IPT-875CB2F8-8C0B-2994-E053-5014A8C0E0B8")
    DIFFUSERList.append("IPT-87BF9F31-AB83-7BB3-E053-5014A8C08E98")
    DIFFUSERList.append("IPT-87F6FC7F-1499-5EF5-E053-5014A8C052EF")
    DIFFUSERList.append("IPT-87FCEC68-84AC-0547-E053-5014A8C07E92")
    DIFFUSERList.append("IPT-87FCF2D2-E12B-0574-E053-5014A8C0E053")
    DIFFUSERList.append("IPT-87FCFAFA-BC57-0572-E053-5014A8C04A0C")
    DIFFUSERList.append("IPT-884FEA17-4810-3B88-E053-5014A8C0FB66")
    DIFFUSERList.append("IPT-8A94A8D1-DD28-45D6-E053-5014A8C0E731")
    DIFFUSERList.append("IPT-8B0E3E09-9937-46A4-E053-5014A8C07D2E")
    DIFFUSERList.append("IPT-8B0E3E09-9938-46A4-E053-5014A8C07D2E")
    DIFFUSERList.append("IPT-8BFADCF5-0007-08E0-E053-5014A8C07AA4")
    DIFFUSERList.append("IPT-8E05E34C-DEDF-69ED-E053-5014A8C03625")
    DIFFUSERList.append("IPT-8EE1F26D-7134-3A46-E053-5014A8C0CEAC")
    DIFFUSERList.append("IPT-90CA324A-CD43-43CA-E053-5014A8C03B1B")
    DIFFUSERList.append("IPT-90CA324A-CD5B-43CA-E053-5014A8C03B1B")
    DIFFUSERList.append("IPT-926B5C8B-81DA-0F0C-E053-5014A8C00278")
    DIFFUSERList.append("IPT-94037605-9E7A-5C85-E053-5014A8C0B110")
    DIFFUSERList.append("IPT-9805AC8A-0F3B-304D-E053-5014A8C01213")
    DIFFUSERList.append("IPT-98F243D9-EFB5-34F7-E053-5014A8C084B6")
    DIFFUSERList.append("IPT-995A5CE5-56DA-486A-E053-5014A8C002E1")
    DIFFUSERList.append("IPT-99937D13-8D05-077B-E053-5014A8C00536")
    DIFFUSERList.append("IPT-9A0EE128-A09E-1AEE-E053-5014A8C0E83E")
    global MAJList
    MAJList.append("IPT-4A9DDA1F-B748-3E13-E053-2614A8C02B7C")
    MAJList.append("IPT-4A9DDA1F-B768-3E13-E053-2614A8C02B7C")
    MAJList.append("IPT-4A9DDA1F-B776-3E13-E053-2614A8C02B7C")
    MAJList.append("IPT-4A9DDA1F-B88E-3E13-E053-2614A8C02B7C")
    MAJList.append("IPT-4A9DDA1F-B8CD-3E13-E053-2614A8C02B7C")
    MAJList.append("IPT-4A9DDA1F-B8FB-3E13-E053-2614A8C02B7C")
    MAJList.append("IPT-4A9DDA1F-B956-3E13-E053-2614A8C02B7C")
    MAJList.append("IPT-4A9DDA1F-B9AE-3E13-E053-2614A8C02B7C")
    MAJList.append("IPT-4A9DDA1F-B9BE-3E13-E053-2614A8C02B7C")
    MAJList.append("IPT-4B288174-EF04-4338-E053-2614A8C07BAF")
    MAJList.append("IPT-4B288174-EF0E-4338-E053-2614A8C07BAF")
    MAJList.append("IPT-4B288174-EF13-4338-E053-2614A8C07BAF")
    MAJList.append("IPT-4B288174-EF18-4338-E053-2614A8C07BAF")
    MAJList.append("IPT-4B288174-EF59-4338-E053-2614A8C07BAF")
    MAJList.append("IPT-4B288174-EF7C-4338-E053-2614A8C07BAF")
    MAJList.append("IPT-4B288174-EF86-4338-E053-2614A8C07BAF")
    MAJList.append("IPT-4B288174-EF90-4338-E053-2614A8C07BAF")
    MAJList.append("IPT-5267B24D-13C4-355B-E053-2614A8C0CBAC")
    MAJList.append("IPT-52F0B9C9-524B-2F80-E053-2614A8C04BB2")
    MAJList.append("IPT-6026F6D4-BFFF-03FC-E053-2614A8C051EE")
    MAJList.append("IPT-6026F6D4-C014-03FC-E053-2614A8C051EE")
    MAJList.append("IPT-602783F1-3367-22CB-E053-2614A8C003AE")
    MAJList.append("IPT-630EA612-B3CB-42E2-E053-2614A8C0CF63")
    MAJList.append("IPT-6703B679-4929-2690-E053-2614A8C08B46")
    MAJList.append("IPT-6917B86D-5077-670E-E053-2614A8C04F91")
    MAJList.append("IPT-7289F131-A159-071C-E053-2614A8C02965")
    MAJList.append("IPT-75D45416-D097-7E25-E053-5014A8C03E45")

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

def registerAll():
    session = login()
    for dr in MAJList:
        register(dr, session)
    for dr in DIFFUSERList:
        register(dr, session)

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
    #checkAll()
    #checkHardAll()
    #publishAll()
    #registerAll()

if __name__ == "__main__":
    #loadDR()
    #loadDRfromList()
    main()
