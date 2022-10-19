import json
import random
import pytest

from uas_standards.en4709_02 import OperatorRegistrationNumber


def test_basic_usage():
    r = random.Random(12345)

    rn = OperatorRegistrationNumber.generate_valid('EXM', r)
    assert rn.valid
    OperatorRegistrationNumber.validate_prefix(rn.prefix)
    OperatorRegistrationNumber.validate_base_id(rn.base_id)
    OperatorRegistrationNumber.validate_final_random_string(rn.final_random_string)

    rn2 = OperatorRegistrationNumber.from_components(rn.prefix, rn.base_id, rn.final_random_string)
    assert rn2.valid
    assert rn2 == rn

    plain_str = json.loads(json.dumps({'rn': rn}))['rn']
    rn3 = OperatorRegistrationNumber(plain_str)
    assert rn3.valid
    assert rn3 == rn

    rn_invalid = rn.make_invalid_by_changing_final_control_string(r)
    assert rn.valid
    assert not rn_invalid.valid
    OperatorRegistrationNumber.validate_prefix(rn_invalid.prefix)
    OperatorRegistrationNumber.validate_base_id(rn_invalid.base_id)
    OperatorRegistrationNumber.validate_final_random_string(rn_invalid.final_random_string)

    with pytest.raises(ValueError):
        OperatorRegistrationNumber.validate_prefix('US')

    OperatorRegistrationNumber.validate_base_id('aaaaaaaaaaaa')
    with pytest.raises(ValueError):
        OperatorRegistrationNumber.validate_base_id('aaaaaaaaaaa')
    with pytest.raises(ValueError):
        OperatorRegistrationNumber.validate_base_id('aaaaaaaaaaaA')

    OperatorRegistrationNumber.validate_final_random_string('aaa')
    with pytest.raises(ValueError):
        OperatorRegistrationNumber.validate_final_random_string('aa')
    with pytest.raises(ValueError):
        OperatorRegistrationNumber.validate_final_random_string('aaA')
