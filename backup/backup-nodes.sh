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

zipBackupIPT "ipt_data_benin" "ipt_data_benin"
zipBackupIPT "ipt_data_botswana" "ipt_data_botswana"
zipBackupIPT "ipt_data_burkina" "ipt_data_burkina"
zipBackupIPT "ipt_data_burundi" "ipt_data_burundi"
zipBackupIPT "ipt_data_cameroun" "ipt_data_cameroun"
zipBackupIPT "ipt_data_cotedivoire" "ipt_data_cotedivoire"
zipBackupIPT "ipt_data_gabon" "ipt_data_gabon"
zipBackupIPT "ipt_data_ghana" "ipt_data_ghana"
zipBackupIPT "ipt_data_guinee" "ipt_data_guinee"
zipBackupIPT "ipt_data_madagascar" "ipt_data_madagascar"
zipBackupIPT "ipt_data_nigeria" "ipt_data_nigeria"
zipBackupIPT "ipt_data_senegal" "ipt_data_senegal"
zipBackupIPT "ipt_data_togo" "ipt_data_togo"
zipBackupIPT "ipt_data_uganda" "ipt_data_uganda"
zipBackupWebsite "drupal-benin-d7" "website_drupal-benin-d7"
zipBackupWebsite "drupal-madbif" "website_drupal-madbif"
zipBackupWebsite "titan" "website_titan"

echo "Backup $DAILY_OR_MONTHLY db_nodes_all..."
mysqldump -u root -p'PASSWORD' --all-databases > /data/backup/latest/db_nodes_all.sql 2> /data/backup/latest/db_nodes_all.log
zip -qr /data/backup/latest/db_nodes_all.zip /data/backup/latest/db_nodes_all.sql /data/backup/latest/db_nodes_all.log
rm /data/backup/latest/db_nodes_all.sql

echo "Backup $DAILY_OR_MONTHLY db_titan..."
mysqldump -u root -p'PASSWORD' --databases titan > /data/backup/latest/db_titan.sql 2> /data/backup/latest/db_titan.log
zip -qr /data/backup/latest/db_titan.zip /data/backup/latest/db_titan.sql /data/backup/latest/db_titan.log
rm /data/backup/latest/db_titan.sql
