import os
import requests
import shutil
import time
import subprocess

LOCAL_PERCENT_FREE              = 25
DIST_PERCENT_FREE               = 25

SLACK_CMD                       = "/data/backup//slack.sh "

LOCAL_PATH                      = "/data/"
LOCAL_DAILY_PATH                = "/data/backup/daily/"
LOCAL_DAILY_D00_PATH            = LOCAL_DAILY_PATH + "d-00/"
LOCAL_MONTHLY_PATH              = "/data/backup/monthly/"
LOCAL_MONTHLY_M0_PATH           = LOCAL_MONTHLY_PATH + "m-0/"
LOCAL_MONTHLY_M0_FRANCE_PATH    = LOCAL_MONTHLY_M0_PATH + "france/"
LOCAL_MONTHLY_M0_NODES_PATH     = LOCAL_MONTHLY_M0_PATH + "nodes/"

DIST_BACKUP_PATH                = "/data/backup/"
SSH_CMD                         = "ssh -i /home/backupgbif/.ssh/fg-backup.pem"
NODES_CONNECTION                = "ubuntu@193.50.94.183"
FRANCE_CONNECTION               = "ubuntu@193.50.94.47"

DISK_USAGE_CMD                  = "du -s "
DISK_USAGE_END_CMD              = " | awk '{print $1}'"
DISK_FREE_CMD                   = "df --output=avail "
DISK_FREE_END_CMD               = " | tail -n 1"

def __size(dir):
    return float(subprocess.check_output(DISK_USAGE_CMD + dir + DISK_USAGE_END_CMD, shell=True, text=True))*1000

def __free(dir):
    return float(shutil.disk_usage(dir)[2])

def __total(dir):
    return float(shutil.disk_usage(dir)[0])

def __localFree(dir):
    return float(subprocess.check_output(DISK_FREE_CMD + dir + DISK_FREE_END_CMD, shell=True, text=True))*1000
    
def __remoteFree(connection, dir):
    return float(subprocess.check_output(__getSSHCmd(connection, DISK_FREE_CMD + dir + DISK_FREE_END_CMD), shell=True, text=True))*1000

def __getSSHCmd(connection, cmd):
    return SSH_CMD + " " + connection + " \"" + cmd + "\""

def __slack(message):
    os.system(SLACK_CMD+" '"+message+"'")

def __formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%.2fG" % (G)
        else:
            return "%.2fM" % (M)
    else:
        return "%.2fkb" % (kb)

def __formatDate(time):
    return time.tm_year + time.tm_mon + time.tm_mday

if __name__ == "__main__":

    localTime = time.localtime()
    localDate = __formatDate(localTime)
    localDay = localTime.tm_mday

    # If m-00 exists, check remaining space
    if os.path.exists(LOCAL_MONTHLY_M0_FRANCE_PATH) and os.path.exists(LOCAL_MONTHLY_M0_NODES_PATH):

        M0_FRANCE = __size(LOCAL_MONTHLY_M0_FRANCE_PATH)
        M0_NODES = __size(LOCAL_MONTHLY_M0_NODES_PATH)
        M0_TOTAL = M0_FRANCE + M0_NODES
        
        # locally
        localFree = __localFree(LOCAL_PATH)
        if M0_TOTAL * (LOCAL_PERCENT_FREE/100) > localFree:
            message = "WARNING ! Only "+__formatSize(localFree)+" remaining on backup-gbif disk (last monthly archive = "+__formatSize(M0_TOTAL)+")"
            print(message)
            __slack(message)

        # dist / france
        distFranceFree = __remoteFree(FRANCE_CONNECTION, DIST_BACKUP_PATH)
        if M0_FRANCE * (DIST_PERCENT_FREE/100) > distFranceFree:
            message = "WARNING ! Only "+__formatSize(distFranceFree)+" remaining on gbif-france disk (last monthly archive = "+__formatSize(M0_FRANCE)+")"
            print(message)
            __slack(message)

        # dist / nodes
        distNodesFree = __remoteFree(NODES_CONNECTION, DIST_BACKUP_PATH)
        if M0_NODES * (DIST_PERCENT_FREE/100) > distNodesFree:
            message = "WARNING ! Only "+__formatSize(distNodesFree)+" remaining on gbif-nodes disk (last monthly archive = "+__formatSize(M0_NODES)+")"
            print(message)
            __slack(message)

    # Check d-00 creation date
    if os.path.exists(LOCAL_DAILY_D00_PATH):
        stat = os.stat(LOCAL_DAILY_D00_PATH)
        lastRunTime = time.gmtime(stat.st_mtime)
        lastRunDate = __formatDate(lastRunTime)
    else:
        lastRunDate = ""

    if localDate == lastRunDate:
        print("Daily archive done.")
    else:
        print("WARNING ! No daily archive done today.")
        __slack("WARNING ! No daily archive done today.")

    # Monthly backup
    if localDay == 1:

        # Check m-0 creation date
        if os.path.exists(LOCAL_MONTHLY_M0_PATH):
            stat = os.stat(LOCAL_MONTHLY_M0_PATH)
            lastRunTime = time.gmtime(stat.st_mtime)
            lastRunDate = __formatDate(lastRunTime)
        else:
            lastRunDate = ""

        if localDate == lastRunDate:
            sizeM0 = __size(LOCAL_MONTHLY_M0_PATH)
            sizeMonthly = __size(LOCAL_MONTHLY_PATH)
            sizeDaily = __size(LOCAL_DAILY_PATH)
            sizeFree = __free(LOCAL_PATH)
            percent = sizeFree * 100 / __total(LOCAL_PATH)
            
            message = "Monthly archive done.\n"+ \
                      "- latest monthly archive = "+__formatSize(sizeM0)+"\n"+ \
                      "- all monthly archives = "+__formatSize(sizeMonthly)+"\n"+ \
                      "- all daily archives = "+__formatSize(sizeDaily)+"\n"+ \
                      "- free space on local = "+__formatSize(sizeFree)+" ("+str(int(percent))+"%)"
            print(message)
            __slack(message)

        else:
            print("WARNING ! No monthly archive done today.")
            __slack("WARNING ! No monthly archive done today.")
