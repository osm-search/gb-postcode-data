#!/usr/bin/env python3

import sys

from csv import DictReader, DictWriter
from lib.convert import normalize_postcode, check_postcode


##
## CSV Input/Output fields
##
fields = ['postcode', 'lat', 'lon']


accumulator = {}

with open("NI-postcodes.csv") as file:
    csv_reader = DictReader(file, fieldnames=fields)
    for row in csv_reader:
        postcode = normalize_postcode(row['postcode'])

        if not check_postcode(postcode):
            print("invalid postcode '%s'" % postcode, file=sys.stderr)
            continue

        lat = float(row['lat'])
        lon = float(row['lon'])
        pc = accumulator.get(postcode)
        if pc is not None:
            accumulator[postcode] = ((pc[0] + lat) / 2, (pc[1] + lon) / 2)
        else:
            accumulator[postcode] = (lat, lon)

    csv_writer = DictWriter(sys.stdout, fieldnames=fields, lineterminator="\n")
    csv_writer.writeheader()

    for postcode, location in accumulator.items():
        csv_writer.writerow({
            'postcode': postcode,
            'lat': '%0.5f' % location[0],
            'lon': '%0.5f' % location[1]
        })
