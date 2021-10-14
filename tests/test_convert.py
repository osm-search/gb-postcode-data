import pytest

from lib.convert import normalize_postcode, check_postcode

def test_normalize_postcode():
    assert normalize_postcode('E8  1LN') == 'E8 1LN'
    assert normalize_postcode('E81LN') == 'E8 1LN'

def test_check_postcode():
    assert check_postcode('N6 5XR') == True
    assert check_postcode('n6 5xr') == False
    assert check_postcode('N65XR') == False
    assert check_postcode('N6') == False
