import requests

IPT_URL             = 'http://ipt-inpn.gbif.fr/'
IPT_USER            = 'sylvain.morin@mnhn.fr'
IPT_PWD             = ''
RESULT_FILE_PATH    = "output/IPT_2020-09-01.csv"
CSV_SEPARATOR       = ";"
UUID_FILE           = '/workspace/ipt-batch-import-inpn/uuid'

uidList = []

#with open(UUID_FILE, newline='') as csvfile:
#    csv_reader = csv.reader(csvfile, delimiter=';')
#    csv_rows = list(csv_reader)
#    for row in csv_rows:
#        uidList.append(row[0])

def generateAllStatusReport():
    generateStatusReport([])

def generateStatusReport(uidList):
    session = __login()
    data = __getDataFromIPT(session)
    out = open(RESULT_FILE_PATH, "w")

    out.write("ID")
    out.write(CSV_SEPARATOR)
    out.write("TITLE")
    out.write(CSV_SEPARATOR)
    out.write("COUNT")
    out.write(CSV_SEPARATOR)
    out.write("MODIFIED")
    out.write(CSV_SEPARATOR)
    out.write("PUBLICATION")
    out.write(CSV_SEPARATOR)
    out.write("REGISTERED")
    out.write(CSV_SEPARATOR)
    out.write("ORGANISATION")
    out.write(CSV_SEPARATOR)
    out.write("URL\n")

    for ds in data:
        print(ds)
        organisation = ds[2]
        count = ds[5]
        modified = ds[6]
        publication = ds[7]

        count = str(count).replace(',', '')

        header = ds[1]
        title = header[header.find("<if>")+4:header.rfind("</a>")]
        url = header[header.find("href='")+6:header.rfind("'>")]
        id = url[(url.rfind('=')+1)::]

        status = "False" if organisation == "Not registered" else "True"

        if (len(uidList) == 0) or (id in uidList):
            out.write(id)
            out.write(CSV_SEPARATOR)
            out.write(title)
            out.write(CSV_SEPARATOR)
            out.write(str(count))
            out.write(CSV_SEPARATOR)
            out.write(modified)
            out.write(CSV_SEPARATOR)
            out.write(publication)
            out.write(CSV_SEPARATOR)
            out.write(status)
            out.write(CSV_SEPARATOR)
            out.write(organisation)
            out.write(CSV_SEPARATOR)
            out.write(url)
            out.write("\n")

    out.close()

def generatePublishedReport(uidList, version, hardCheck):
    session = __login()
    data = __getDataFromIPT(session)
    out = open(RESULT_FILE_PATH, "w")

    out.write("ID")
    out.write(CSV_SEPARATOR)
    out.write("PUBLISHED_CHECK")
    if hardCheck:
        out.write(CSV_SEPARATOR)
        out.write("PUBLISHED_HARD_CHECK")
    out.write("\n")

    for ds in data:
        header = ds[1]
        title = header[header.find("<if>")+4:header.rfind("</a>")]
        url = header[header.find("href='")+6:header.rfind("'>")]
        id = url[(url.rfind('=')+1)::]

        if (len(uidList) == 0) or (id in uidList):
            out.write(id)
            out.write(CSV_SEPARATOR)

            isPublished = __checkPublished(id, version, session)
            out.write(str(isPublished))

            if hardCheck:
                out.write(CSV_SEPARATOR)
                isHardPublished = __checkHardPublished(id, version, session)
                out.write(str(isHardPublished))

            out.write("\n")

    out.close()

def __checkPublished(uid, version, session):
    responseCheck = session.get(IPT_URL + 'publicationlog.do?r='+uid)
    if responseCheck.status_code == 200:
        if ("Archive version #"+version+" generated successfully!" in responseCheck.text):
            return True
    return False

def __checkHardPublished(uid, version, session):
    responseCheck = session.get(IPT_URL + 'manage/resource?r='+uid)
    if responseCheck.status_code == 200:
        if ("<th>Version</th><td class=\"separator green\">"+version+"&nbsp;" in responseCheck.text):
            return True
    return False

def __getDataFromIPT(session):
    responseCheck = session.get(IPT_URL + 'manage')
    text = responseCheck.text

    start = "var aDataSet = ["
    end = "];"
    startID = text.find(start)+len(start)
    endID = text.find(end, startID)

    data = "[" + text[startID:endID] + "]"

    return eval(data)

def __login():
    session = requests.Session()
    session.post(IPT_URL)
    data = {"email": IPT_USER, "password": IPT_PWD, "csrfToken": session.cookies['CSRFtoken'], "portal.login": "login"}
    session.post(IPT_URL + 'login.do', data=data)
    return session

if __name__ == "__main__":
    generateAllStatusReport()
