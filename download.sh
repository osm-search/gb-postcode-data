#!/bin/bash

# If the redirect doesn't work, then downlod manually from
# https://osdatahub.os.uk/downloads/open/CodePointOpen

wget -O codepo_db.zip 'https://api.os.uk/downloads/v1/products/CodePointOpen/downloads?area=GB&format=CSV&redirect'

unzip codepo_db.zip
