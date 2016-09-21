import sys
import numpy as np
from MulensModel.mulensdata import MulensData


for path in sys.path:
    if path.find("MulensModel") > 0:
        MODULE_PATH = "/".join(path.split("/")[:-1])
SAMPLE_FILE_01 = MODULE_PATH + "/data/phot_ob08092_O4.dat"

def test_file_read():
    '''read sample file and check if values match'''
    data = MulensData(file_name=SAMPLE_FILE_01)

    np.testing.assert_almost_equal(data.time[0], 5264.84100, err_msg="time of first line doesn't match")
    
    assert data.mag[-1] == 13.913, "magnitude of the last line doesn't match"


def test_get_jd_zeropoint_1():
    test_data = MulensData()
    assert test_data._get_jd_zeropoint(7500.) == 2450000.

def test_get_jd_zeropoint_2():
    test_data = MulensData()
    assert test_data._get_jd_zeropoint(np.array((7500.,7501.))) == 2450000.

def test_get_jd_zeropoint_3():
    test_data = MulensData()
    assert test_data._get_jd_zeropoint(np.array((57500.,57501.))) == 2400000.

def test_get_jd_zeropoint_4():
    test_data = MulensData()
    assert test_data._get_jd_zeropoint(np.array((9999.,10000.))) == 2450000.

def test_get_jd_zeropoint_5():
    test_data = MulensData()
    assert test_data._get_jd_zeropoint(np.array((2457500.,2457501.))) == 0.

def test_get_jd_zeropoint_6():
    test_data = MulensData()
    try:
        assert test_data._get_jd_zeropoint(np.array((np.nan, np.nan))) == 0.
    except ValueError:
        assert 1==1


