#!/bin/bash

python3.7 /data/backup/backup.py > /data/backup/logs/backup.log
python3.7 /data/backup/report-backup.py > /data/backup/logs/report.log
