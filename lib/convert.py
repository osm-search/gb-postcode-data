import re
import math

# https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Validation
# but changed ' ?' to ' ' because we want to enforce the space
REGEX_VALID_POSTCODE = '^(([A-Z]{1,2}[0-9][A-Z0-9]?|ASCN|STHL|TDCU|BBND|[BFS]IQQ|PCRN|TKCA) [0-9][A-Z]{2}|BFPO ?[0-9]{1,4}|(KY[0-9]|MSR|VG|AI)[ -]?[0-9]{4}|[A-Z]{2} ?[0-9]{2}|GE ?CX|GIR ?0A{2}|SAN ?TA1)$'

def normalize_postcode(postcode):
    # multiple space to one
    postcode = re.sub(r'\s+', ' ', postcode)

    # add space if needed
    postcode = re.sub(r'(\S)(\d[A-Z][A-Z])$', '\\1 \\2', postcode)
    return postcode

def check_postcode(postcode):
    return bool(re.match(REGEX_VALID_POSTCODE, postcode))

# https://janakiev.com/blog/gps-points-distance-python/
# returns distance in meters
def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2

    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))