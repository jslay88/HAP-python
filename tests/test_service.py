"""
Tests for pyhap.service
"""
import uuid

import pytest

import pyhap.service as service
from pyhap.characteristic import Characteristic, HAP_FORMAT, HAP_PERMISSIONS
from pyhap.accessory import IIDManager

CHAR_PROPS = {
    "Format": HAP_FORMAT.INT,
    "Permissions": HAP_PERMISSIONS.READ,
}


def get_chars():
    c1 = Characteristic("Char 1", uuid.uuid1(), CHAR_PROPS)
    c2 = Characteristic("Char 2", uuid.uuid1(), CHAR_PROPS)
    return [c1, c2]


def test_add_characteristic():
    serv = service.Service(uuid.uuid1(), "Test Service")
    chars = get_chars()
    serv.add_characteristic(*chars)
    for c in chars:
        assert serv.get_characteristic(c.display_name, check_optional=False) == c


def test_add_opt_characteristic():
    serv = service.Service(uuid.uuid1(), "Test Service")
    chars = get_chars()
    serv.add_opt_characteristic(*chars)
    for c in chars:
        assert serv.get_characteristic(c.display_name, check_optional=True) == c


def test_to_HAP():
    serv = service.Service('83B45914-1861-11E8-85E7-1C1B0D902B9B', 'Test Service')
    iid = IIDManager()
    hap_rep = serv.to_HAP(iid)
    print(hap_rep, flush=True)
    assert (hap_rep['iid'] is None
            and hap_rep['type'] == '83B45914-1861-11E8-85E7-1C1B0D902B9B'
            and hap_rep['characteristics'] == [])
