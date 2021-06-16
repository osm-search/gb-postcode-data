GB Postcode data for Nominatim
==============================

The Nominatim server [import instructions](https://www.nominatim.org/release-docs/latest/admin/Import/)
allow optionally download `gb_postcodes.csv.gz`. This document explains how the file gets created. Data
is updated several times per year.

Note: Nominatim version 3.7 and earlier used database dump files (`gb_postcode_data.sql.gz`) instead. If
you want to generate those check out the [`sql-file-generation` tag](https://github.com/osm-search/gb-postcode-data/tags).


GB vs UK
--------
GB (Great Britain) is more correct as the Ordnance Survey dataset doesn't contain postcodes from
Northern Ireland.



Code-Point Open data
--------------------

Ordnance Survey, the national mapping agency for Great Britain, publishes an open dataset at
https://osdatahub.os.uk/downloads/open/CodePointOpen



Converting Code-Point Open data
-------------------------------

1. Install dependencies.

        # assuming Ubuntu
        $ apt-get install unzip python3
        $ pip3 install pyproj csv

2. Run `download.sh`. It will download and extract the raw data

     You'll see a directory of CSV files.

        # should be about 1.7 million lines
        $ cat codepo_gb/Data/CSV/*.csv | wc -l

        $ more codepo_gb/Data/CSV/n.csv
        "N1 0AA",10,530626,183961,"E92000001","E19000003","E18000007","","E09000019","E05000368"
        "N1 0AB",10,530559,183978,"E92000001","E19000003","E18000007","","E09000019","E05000368"

    The coordinates are "Northings" and "Eastings" in [OSGB 1936](http://epsg.io/27700) projection.

3. Run `convert.py`

        convert.py > gb_postcode_data.sql
        wc -l gb_postcode_data.sql
        gzip -9 gb_postcode_data.sql


License
-------
The source code is available under a GPLv2 license.
