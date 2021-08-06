UK Postcode data for Nominatim
==============================

The Nominatim server supports importing additional postcodes per country from comma-separated files,
see [import instructions](https://www.nominatim.org/release-docs/latest/admin/Import/). This document
described how the file `gb_postcodes.csv.gz` gets created.

Older versions of Nominatim supported database dump files (`gb_postcode_data.sql.gz`) instead. If
you want to generate those check out the older [`sql-file-generation`](https://github.com/osm-search/gb-postcode-data/tags) tag of this repository.


Data sources and license
------------------------

Data consists of

1. Code-Point® Open for England, Scotland, Wales with about 1.7 million postcodes

   [Ordnance Survey](https://en.wikipedia.org/wiki/Ordnance_Survey), the national mapping agency
   for Great Britain, publishes the open dataset four times per year at
   https://osdatahub.os.uk/downloads/open/CodePointOpen

2. About 15.000 Northern Ireland postcodes

        https://github.com/osm-uk/NI-Postcodes derived from Food Hygiene Ratings Scheme Data
        sets.

Both are licensed under [Open Government Licence (v3)](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).



GB vs UK
--------

Great Britain is England, Scotland, Wales.

United Kingdom is England, Scotland, Wales, Northern Ireland.

For probably historical reasons the the ISO-3166 country code for the United Kingdom is 'GB'. Nominatim,
and OpenStreetMap database in general, expects 'gb' thus the output filename contains 'gb'.





Creating the file
-----------------

1. Install dependencies

        # assuming Ubuntu
        apt-get install unzip python3
        pip3 install pyproj

2. Download source files

        ./download.sh

     You'll see a directory of CSV files.

        cat code_gb/Data/CSV/*.csv | wc -l

        more Data/CSV/n.csv
        "N1 0AA",10,530626,183961,"E92000001","E19000003","E18000007","","E09000019","E05000368"
        "N1 0AB",10,530559,183978,"E92000001","E19000003","E18000007","","E09000019","E05000368"

    The coordinates are "Northings" and "Eastings" in [OSGB 1936](http://epsg.io/27700) projection.

3. Convert data

        ./convert.py > gb_postcodes.csv
        grep -v postcode NI-postcodes.csv >> gb_postcodes.csv

        # expect about 1.7m
        wc -l gb_postcodes.csv

        gzip -9 gb_postcodes.csv
        # expect 13M
        ls -lah

4. Cleanup source files

        rm -r codepo_gb.zip codepo_gb NI-postcodes.csv

License
-------
The source code is available under a GPLv2 license.
