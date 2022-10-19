import json
import random

from uas_standards.ansi_cta_2063_a import SerialNumber


def test_basic_usage():
    r = random.Random(12345)

    sn = SerialNumber.generate_valid(r)
    assert sn.valid

    sn2 = SerialNumber.from_components(sn.manufacturer_code, sn.manufacturer_serial_number)
    assert sn2.valid
    assert sn2 == sn

    plain_str = json.loads(json.dumps({'sn': sn}))['sn']
    sn3 = SerialNumber(plain_str)
    assert sn3.valid
    assert sn3 == sn

    sn_invalid = sn.make_invalid_by_changing_payload_length(r)
    assert sn.valid
    assert not sn_invalid.valid
