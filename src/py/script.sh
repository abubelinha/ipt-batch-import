
docker run  -v /tmp/IPTMAJ/dataset:/dataset -v /tmp/IPTMAJ/result:/result -v /tmp/IPTMAJ/identifiers.csv:/identifiers.csv gbiffrance/ipt-bath-import:1.0

# create uuid array
for f in IPT-* ; do echo $f ; done > uuid

# get list
scp  -i /home/sylmorin/.ssh/fg-gbif ubuntu@193.50.94.47:/data/IPT_MAJ_2020-05-13/result/uuid .

# check
for f in IPT-* ; do grep key $f/resource.xml ; done

# backup
for f in IPT-* ; do sudo mv /data/www/private/ipt/ipt_data_inpn/resources/$f /data/IPT_MAJ_2020-05-13/backup ; done

# copy
for f in IPT-* ; do sudo cp -R $f /data/www/private/ipt/ipt_data_inpn/resources/ ; done

# owner/right
for f in /data/www/private/ipt/ipt_data_inpn/resources/* ; do sudo chmod 775 -Rf $f ; done
for f in /data/www/private/ipt/ipt_data_inpn/resources/* ; do sudo chown tomcat8:tomcat8 -Rf $f ; done






Pipeline 1:
- read folder with ZIP file from Mathieu
- for each ZIP, get UUID

- call IPT http://ipt-inpn.gbif.fr/resource?r=IPT-6C62C6AA-2883-5AE0-E053-2614A8C0C02
  extract GBIF URL
    <a href="http://www.gbif.org/dataset/9d1a3db7-b8a8-4936-9159-4548a7d9e535" class="icon icon-gbif">GBIF</a>
    OR (check file resource.xml in IPT folder and extract <key>)

- extract GBIF UUID from URL
- call GBIF API to check GBIF UUID
- call IPT to check Publish and Register status ???


- execute docker transform to generate IPT folder with correct GBIF UUID if UPDATE

- stop IPT

- backup IPT folder for the dataset (move)
- copy folder of new dataset
- chown / chmod

- restart IPT

- call IPT http://ipt-inpn.gbif.fr/resource?r=IPT-6C62C6AA-2883-5AE0-E053-2614A8C0C02 [CHECK]

- call publish

- hard check publish

- call register

- hard check register

- call GBIF API to check register

- publish report
