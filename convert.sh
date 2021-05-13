#!/bin/bash

POSTGRES_DBNAME=create_gb_postcode_file
POSTGRES_USER=postgres
WORKDIR=/data

echo
echo "* Create database"
createdb --user $POSTGRES_USER $POSTGRES_DBNAME
echo 'CREATE EXTENSION postgis' | psql --user $POSTGRES_USER $POSTGRES_DBNAME


echo
echo "* Download table schema and create table"
wget --quiet -O $WORKDIR/postcode_tables.sql https://raw.githubusercontent.com/osm-search/Nominatim/master/lib-sql/postcode_tables.sql
cat $WORKDIR/postcode_tables.sql | psql --user $POSTGRES_USER $POSTGRES_DBNAME


echo
echo "* Looking for data"
echo "$(ls $WORKDIR/*.csv | wc -l) files"
echo "$(cat $WORKDIR/*.csv | wc -l) lines (should be about 1.7 million)"


echo
echo "* Convert data and load into database"
cat $WORKDIR/*.csv | ./convert_codepoint.php | psql --user $POSTGRES_USER $POSTGRES_DBNAME


echo
echo "* Dump database table into files"
echo '' > gb_postcode_data.sql
if [[ -e $WORKDIR/licence.txt ]]; then
  cat $WORKDIR/licence.txt | iconv -f iso-8859-1 -t utf-8 | dos2unix | sed 's/^/-- /g' >> $WORKDIR/gb_postcode_data.sql
fi
echo "  * gb_postcode_data.sql"
pg_dump --user $POSTGRES_USER --dbname $POSTGRES_DBNAME --table gb_postcode --data-only | grep -v '^--' >> $WORKDIR/gb_postcode_data.sql
echo "  * gb_postcodes.csv"
psql --user $POSTGRES_USER --dbname $POSTGRES_DBNAME -A -F"," -c 'SELECT postcode, ST_Y(geometry) as y, ST_X(geometry) as x FROM gb_postcode' > $WORKDIR/gb_postcodes.csv

echo
echo "* Compress output files"
gzip -9 -f $WORKDIR/gb_postcode_data.sql
gzip -9 -f $WORKDIR/gb_postcodes.csv
ls -l $WORKDIR/gb_*.*


echo
echo "* Cleanup"
dropdb --user $POSTGRES_USER $POSTGRES_DBNAME
rm $WORKDIR/postcode_tables.sql
