import pytest
from slcwindinversion.utils import get_l2_filepath

inputs_l1b = [
    "/tmp/data/products/tests/iw/slc/l1b/4.0.0/S1B_IW_XSP__1SDV_20210420T094117_20210420T094144_026549_032B99_2058.SAFE/s1b-iw1-slc-vv-20210420t094118-20210420t094144-026549-032b99-004_L1B_xspec_IFR_4.0.0.nc",
    "/tmp/data/products/tests/iw/slc/l1b/4.0.0/S1B_IW_XSP__1SDV_20210420T094117_20210420T094144_026549_032B99_2058_A03.SAFE/s1b-iw1-slc-vv-20210420t094118-20210420t094144-026549-032b99-004_L1B_xspec_IFR_4.0.0.nc",
]
expected_l1c = [
    "/tmp/2021/110/S1B_IW_XSP__1SDV_20210420T094117_20210420T094144_026549_032B99_2058_B02.SAFE/s1b-iw1-slc-vv-20210420t094118-20210420t094144-026549-032b99-004_L1C_xspec_IFR_B02.nc"
]


@pytest.mark.parametrize(
    ["l1b_fullpath", "expected_l1c"],
    (
        pytest.param(inputs_l1b[0], expected_l1c[0]),
        pytest.param(inputs_l1b[1], expected_l1c[0]),
    ),
)
def test_outputfile_path(l1b_fullpath, expected_l1c):
    version = "C02"
    outputdir = "/tmp/"
    output_format = "nc"
    l1c_full_path = get_l2_filepath(
        l1b_fullpath, version=version, outputdir=outputdir, format=output_format
    )

    print(l1c_full_path)
    assert l1c_full_path == expected_l1c
