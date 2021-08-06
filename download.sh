#!/bin/bash

# If the redirect doesn't work, then downlod manually from
# https://osdatahub.os.uk/downloads/open/CodePointOpen

wget -O codepo_gb.zip 'https://api.os.uk/downloads/v1/products/CodePointOpen/downloads?area=GB&format=CSV&redirect'
unzip -q -o -d codepo_gb codepo_gb.zip


wget --no-clobber https://raw.githubusercontent.com/osm-uk/NI-Postcodes/main/data/NI-postcodes.csv


echo "England, Scotland, Wales: "
cat codepo_gb/Data/CSV/*.csv | wc -l

echo "Northern Ireland: "
wc -l NI-postcodes.csv
