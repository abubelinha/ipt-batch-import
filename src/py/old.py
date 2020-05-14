
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

