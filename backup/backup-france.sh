#!/bin/bash

if [ "$1" = "" ]; then
  echo "Please enter daily or monthly"
  exit
fi 

DAILY_OR_MONTHLY=$1
DATE_FILE=/data/backup/latest/`echo $DAILY_OR_MONTHLY`_`date +%Y-%m-%d_%H:%M:%S`

rm -Rf /data/backup/latest/
mkdir -p /data/backup/latest/

touch $DATE_FILE  

zipBackupIPT() {
  echo "Backup $DAILY_OR_MONTHLY $2..."
  if [ $DAILY_OR_MONTHLY = "daily" ]
  then
    zip -r /data/backup/latest/$2.zip $DATE_FILE `find /data/www/private/ipt/$1/ -type f -mtime -1` -x '/data/www/private/ipt/'$1'/logs/*' -x '/data/www/private/ipt/'$1'/tmp/*'
  else
    zip -rq /data/backup/latest/$2.zip $DATE_FILE /data/www/private/ipt/$1/ -x '/data/www/private/ipt/'$1'/logs/*' -x '/data/www/private/ipt/'$1'/tmp/*'
  fi 
}

zipBackupWebsite() {
  echo "Backup $DAILY_OR_MONTHLY $2..."
  if [ $DAILY_OR_MONTHLY = "daily" ]
  then
    zip -r /data/backup/latest/$2.zip $DATE_FILE `find /data/www/html/$1/ -type f -mtime -1`
  else
    zip -rq /data/backup/latest/$2.zip $DATE_FILE /data/www/html/$1/
  fi 
}

zipBackupIPT "ipt_data" "ipt_data_france"
zipBackupIPT "ipt_data_inpn"  "ipt_data_inpn"
zipBackupWebsite "site-gbif" "website_site-gbif"
zipBackupWebsite "photos" "website_photos"
zipBackupWebsite "chamilo" "website_chamilo"

echo "Backup $DAILY_OR_MONTHLY db_france_all..."
mysqldump -u root -p'PASSWORD' --all-databases > /data/backup/latest/db_france_all.sql 2> /data/backup/latest/db_france_all.log
zip -qr /data/backup/latest/db_france_all.zip /data/backup/latest/db_france_all.sql /data/backup/latest/db_france_all.log
rm /data/backup/latest/db_france_all.sql
