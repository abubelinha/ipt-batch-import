import os
import shutil
import time

LOCAL_DAILY_PATH                = "/data/backup/daily/"
LOCAL_DAILY_D00_PATH            = LOCAL_DAILY_PATH + "d-00/"
LOCAL_DAILY_D00_FRANCE_PATH     = LOCAL_DAILY_D00_PATH + "france/"
LOCAL_DAILY_D00_NODES_PATH      = LOCAL_DAILY_D00_PATH + "nodes/"
LOCAL_MONTHLY_PATH              = "/data/backup/monthly/"
LOCAL_MONTHLY_M0_PATH           = LOCAL_MONTHLY_PATH + "m-0/"
LOCAL_MONTHLY_M0_FRANCE_PATH    = LOCAL_MONTHLY_M0_PATH + "france/"
LOCAL_MONTHLY_M0_NODES_PATH     = LOCAL_MONTHLY_M0_PATH + "nodes/"

RSYNC_CMD                       = "rsync -a -e 'ssh -i /home/backupgbif/.ssh/fg-backup.pem'"
SSH_CMD                         = "ssh -i /home/backupgbif/.ssh/fg-backup.pem"
NODES_CONNECTION                = "ubuntu@193.50.94.183"
FRANCE_CONNECTION               = "ubuntu@193.50.94.47"
DIST_BACKUP_CMD                 = "/data/backup/backup.sh"
DIST_BACKUP_DAILY_CMD           = DIST_BACKUP_CMD + " daily"
DIST_BACKUP_MONTHLY_CMD         = DIST_BACKUP_CMD + " monthly"
DIST_BACKUP_PATH                = "/data/backup/latest/"

#############
#   DAILY
#############

def rotateDaily():
    __print("Rotating daily folders...")

    __rmdir(LOCAL_DAILY_PATH+"d-20")
    __rotate(LOCAL_DAILY_PATH+"d-19", LOCAL_DAILY_PATH+"d-20")
    __rotate(LOCAL_DAILY_PATH+"d-18", LOCAL_DAILY_PATH+"d-19")
    __rotate(LOCAL_DAILY_PATH+"d-17", LOCAL_DAILY_PATH+"d-18")
    __rotate(LOCAL_DAILY_PATH+"d-16", LOCAL_DAILY_PATH+"d-17")
    __rotate(LOCAL_DAILY_PATH+"d-15", LOCAL_DAILY_PATH+"d-16")
    __rotate(LOCAL_DAILY_PATH+"d-14", LOCAL_DAILY_PATH+"d-15")
    __rotate(LOCAL_DAILY_PATH+"d-13", LOCAL_DAILY_PATH+"d-14")
    __rotate(LOCAL_DAILY_PATH+"d-12", LOCAL_DAILY_PATH+"d-13")
    __rotate(LOCAL_DAILY_PATH+"d-11", LOCAL_DAILY_PATH+"d-12")
    __rotate(LOCAL_DAILY_PATH+"d-10", LOCAL_DAILY_PATH+"d-11")
    __rotate(LOCAL_DAILY_PATH+"d-09", LOCAL_DAILY_PATH+"d-10")
    __rotate(LOCAL_DAILY_PATH+"d-08", LOCAL_DAILY_PATH+"d-09")
    __rotate(LOCAL_DAILY_PATH+"d-07", LOCAL_DAILY_PATH+"d-08")
    __rotate(LOCAL_DAILY_PATH+"d-06", LOCAL_DAILY_PATH+"d-07")
    __rotate(LOCAL_DAILY_PATH+"d-05", LOCAL_DAILY_PATH+"d-06")
    __rotate(LOCAL_DAILY_PATH+"d-04", LOCAL_DAILY_PATH+"d-05")
    __rotate(LOCAL_DAILY_PATH+"d-03", LOCAL_DAILY_PATH+"d-04")
    __rotate(LOCAL_DAILY_PATH+"d-02", LOCAL_DAILY_PATH+"d-03")
    __rotate(LOCAL_DAILY_PATH+"d-01", LOCAL_DAILY_PATH+"d-02")
    __rotate(LOCAL_DAILY_PATH+"d-00", LOCAL_DAILY_PATH+"d-01")
    os.makedirs(LOCAL_DAILY_PATH+"d-00")

def createDailyD00():
    __print("Creating daily d-00...")

    __print("Execute daily d-00 on gbif-france...")
    cmd1 = __getSSHCmd(FRANCE_CONNECTION, DIST_BACKUP_DAILY_CMD)
    __os_system(cmd1)
    __print("Retrieve daily d-00 from gbif-france...")
    cmd2 = __getDistFilesCmd(FRANCE_CONNECTION, DIST_BACKUP_PATH, LOCAL_DAILY_D00_FRANCE_PATH)
    __os_system(cmd2)

    __print("Execute daily d-00 on gbif-nodes...")
    cmd3 = __getSSHCmd(NODES_CONNECTION, DIST_BACKUP_DAILY_CMD)
    __os_system(cmd3)
    __print("Retrieve daily d-00 from gbif-nodes...")
    cmd4 = __getDistFilesCmd(NODES_CONNECTION, DIST_BACKUP_PATH, LOCAL_DAILY_D00_NODES_PATH)
    __os_system(cmd4)

##############
#   MONTHLY
##############

def rotateMonthly():
    __print("Rotating monthly folders...")
    
    __rmdir(LOCAL_MONTHLY_PATH+"m-2")
    __rotate(LOCAL_MONTHLY_PATH+"m-1", LOCAL_MONTHLY_PATH+"m-2")
    __rotate(LOCAL_MONTHLY_PATH+"m-0", LOCAL_MONTHLY_PATH+"m-1")
    os.makedirs(LOCAL_MONTHLY_PATH+"m-0")

def createMonthlyM0():
    __print("Creating monthly m-0...")

    __print("Execute monthly d-00 on gbif-france...")
    cmd1 = __getSSHCmd(FRANCE_CONNECTION, DIST_BACKUP_MONTHLY_CMD)
    __os_system(cmd1)
    __print("Retrieve monthly d-00 from gbif-france...")
    cmd2 = __getDistFilesCmd(FRANCE_CONNECTION, DIST_BACKUP_PATH, LOCAL_MONTHLY_M0_FRANCE_PATH)
    __os_system(cmd2)

    __print("Execute monthly d-00 on gbif-nodes...")
    cmd3 = __getSSHCmd(NODES_CONNECTION, DIST_BACKUP_MONTHLY_CMD)
    __os_system(cmd3)
    __print("Retrieve monthly d-00 from gbif-nodes...")
    cmd4 = __getDistFilesCmd(NODES_CONNECTION, DIST_BACKUP_PATH, LOCAL_MONTHLY_M0_NODES_PATH)
    __os_system(cmd4)
    
##############
#   INTERNAL
##############

def __getSSHCmd(connection, cmd):
    return SSH_CMD + " " + connection + " \'" + cmd + "\'"

def __getDistFilesCmd(connection, source, destination):
    return RSYNC_CMD + " " + \
           connection + ":" + source + " " + destination

def __os_system(cmd):
    #print(cmd)
    os.system("/bin/bash -c \"" + cmd + "\"")

def __rmdir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)

def __rotate(fromDir, toDir):
    if os.path.exists(fromDir):
        os.rename(fromDir, toDir)

def __print(message):
    print("[BACKUP] "+ message)

if __name__ == "__main__":

    localDay = time.localtime().tm_mday
    
    # Check d-00 creation date
    if os.path.exists(LOCAL_DAILY_D00_PATH):
        stat = os.stat(LOCAL_DAILY_D00_PATH)
        lastRunDay = time.gmtime(stat.st_mtime).tm_mday
    else:
        lastRunDay = -1
        
    if localDay == lastRunDay:
        __print("Already executed today. Exiting.")
    else:

        __print("Daily backup...")
        rotateDaily()
        createDailyD00()
        
        # Monthly backup
        if localDay == 1:
            __print("Monthly backup...")
            rotateMonthly()
            createMonthlyM0()
