#!/usr/bin/env python3

import sys
import glob

from csv import DictReader, DictWriter
from pyproj import Transformer
from lib.convert import normalize_postcode, check_postcode

##
## CSV Input
##

in_filenames = sorted(glob.glob('codepo_gb/Data/CSV/*.csv'))

# 10 columns but we only need the first 4
in_fieldnames = ['postcode', 'positional_quality_indicator', 'eastings', 'northings']


##
## Transform
##
# We convert OSGB 1936 (https://epsg.io/27700) to WGS 84 (https://epsg.io/4326)
transformer = Transformer.from_crs('EPSG:27700', 'EPSG:4326')


##
## CSV Output
##
out_filenames = ['postcode', 'lat', 'lon']

csv_writer = DictWriter(sys.stdout, fieldnames=out_filenames, lineterminator="\n")
csv_writer.writeheader()




for fieldname in in_filenames:
    with open(fieldname) as file:
        csv_reader = DictReader(file, fieldnames=in_fieldnames)
        for row in csv_reader:
            # Starting Proj version 6 the order of the coordinates changed
            latitude, longitude = transformer.transform(row['eastings'], row['northings'])

            postcode = normalize_postcode(row['postcode'])

            if not check_postcode(postcode):
                print("invalid postcode '%s'" % postcode, File=sys.stderr)
                continue

            csv_writer.writerow({
                'postcode': postcode,
                'lat': '%0.5f' % latitude,
                'lon': '%0.5f' % longitude
            })
