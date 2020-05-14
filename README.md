# IPT Batch Import

A Java "script" to semi-automate producing IPT data directories, for bulk imports of Darwin Core Archives into the IPT.

## Usage

You will need to edit the meta.xml and resource.ftl templates according to the structure of your data, and the
email address and publishing organization key found in IptBulkImport.

Then build the project:

`mvn clean compile`

Then run it using the script:

`./convert-dwca-to-ipt /path/to/my/datasets`

where `/path/to/my/datasets` is the path containing the DwC archives

The results will be available in the `./results` folder
 
Then, copy the resulting directories (with reasonable new names) to your IPT's resource directory, and restart the IPT.

## Docker

Build the Docker image:

`docker build -t ipt-batch-import .`

Execute the batch import:

`
`

* `/path/to/my/datasets` is the host path containing the DwC archives
* `/path/to/my/results` is the host path where the results will be written by the docker container 
* `/path/to/my/identifiers.csv` is the host path of the identifiers.csv file containing the GBIF UUID

