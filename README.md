GB Postcode data for Nominatim
==============================

The Nominatim server [import instructions](https://www.nominatim.org/release-docs/latest/admin/Import/)
allow optionally download [`gb_postcode_data.sql.gz`](https://www.nominatim.org/data/gb_postcode_data.sql.gz).
This document explains how the file gets created. Data is updated several times per year.


GB vs UK
--------
GB (Great Britain) is more correct as the Ordnance Survey dataset doesn't contain postcodes from Northern
Ireland.


Importing separately after the initial import
---------------------------------------------

If you forgot to download the file, or have a new version, you can import it separately:

1. Import the downloaded `gb_postcode_data.sql.gz` file.

2. Run the SQL query `SELECT count(getorcreate_postcode_id(postcode)) FROM gb_postcode;`. This
   will update the search index.

3. Run `utils/setup.php --calculate-postcodes` from the build directory. This will copy data
   form the `gb_postcode` table to the `location_postcodes` table.



Converting Code-Point Open data
-------------------------------

1. Download from [Code-Point® Open](https://osdatahub.os.uk/downloads/open/CodePointOpen)
   data (select 'CSV').

2. Extract the downloaded file.

        unzip codepo_gb.zip

     You'll see a directory of CSV files.

        $ more codepo_gb/Data/CSV/n.csv
        "N1 0AA",10,530626,183961,"E92000001","E19000003","E18000007","","E09000019","E05000368"
        "N1 0AB",10,530559,183978,"E92000001","E19000003","E18000007","","E09000019","E05000368"

    The coordinates are "Northings" and "Eastings" in [OSGB 1936](http://epsg.io/1314)
    projection. They can be projected to WGS84 like this

        SELECT ST_AsText(ST_Transform(ST_SetSRID('POINT(530626 183961)'::geometry,27700), 4326));
        POINT(-0.117872733220225 51.5394424719303)

    [Position on OpenStreetMap](https://osm.org/?mlon=-0.117872&mlat=51.539442)


3. Create a working directory and place the downloaded files in there

        mkdir workdir
        cp codepo_gb/Data/CSV/*.csv workdir
        cp codepo_gb/Doc/licence.txt workdir

4. Convert CSV files into a .sql database dump file

    That includes creating a database, table, import the files, add geometry column,
    dump the file, delete the database.

    Option A:

    * Install Postgresql and other required packages, e.g. on Ubuntu

            apt-get install -y postgresql-12-postgis-3 php unzip dos2unix
       
    * Edit the `convert.sh` script with your database user name and paths and run the script

    Option B:
    
    * Use Docker
    
            docker build --tag gb-postcode-data-convert .

            docker run --detach \
                       --name gb-postcode-data-converter \
                       --env POSTGRES_PASSWORD=sEKr3tT \
                       --volume $PWD/workdir:/data \
                       gb-postcode-data-convert

            sleep 10 # wait for postgresql to be ready

            docker exec -t gb-postcode-data-converter /app/convert.sh

5. Now you have new files `gb_postcode_data.sql.gz` and `gb_postcodes.sql.gz` in your working directory.

6. Cleanup

            docker container rm --force gb-postcode-data-converter
            rm -r workdir
    

License
-------
The source code is available under a GPLv2 license.
