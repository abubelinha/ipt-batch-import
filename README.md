# IPT Batch Import

A Java "script" to semi-automate producing IPT data directories, for bulk imports of Darwin Core Archives into the IPT.

## Usage

You will need to edit the meta.xml and resource.ftl templates according to the structure of your data, and the
email address and publishing organization key found in IptBulkImport.

Then build the project:

`mvn clean compile`

Then run it using the script, with Darwin Core Archives as filenames:

`./convert-dwca-to-ipt ~/4A9DDA1F-B879-3E13-E053-2614A8C02B7C.zip`

And copy the resulting directory (with a reasonable new name) to your IPT's resource directory, and restart the IPT.
