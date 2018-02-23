"""
Tests for pyhap.accessory
"""
import pytest
import re

import pyhap.accessory as accessory
import pyhap.loader as loader


class TestAccessory(object):

    def test_init(self):
        acc = accessory.Accessory("Test Accessory")

    def test_publish_no_broker(self):
        acc = accessory.Accessory("Test Accessory")
        service = loader.get_serv_loader().get("TemperatureSensor")
        char = service.get_characteristic("CurrentTemperature")
        acc.add_service(service)
        char.set_value(25, should_notify=True)

    def test_setup_id(self):
        pattern = re.compile('[A-Z0-9]{4}')
        acc = accessory.Accessory('Test Accessory')
        assert pattern.match(acc.setup_id) is not None

    def test_pincode(self):
        pattern = re.compile(b'\d{3}-\d{2}-\d{3}')
        acc = accessory.Accessory('Test Accessory')
        assert pattern.match(acc.pincode) is not None

    def test_xhm_uri(self):
        """
        Set ``pincode`` on ``Accessory`` to enforce persistent ``encoded_payload`` for testing.
        Allow ``setup_id`` to be randomly generated.
        """
        acc = accessory.Accessory('Test Accessory', pincode=bytearray(b'123-45-678'))
        outlet = accessory.Accessory('Test Accessory', pincode=bytearray(b'123-45-678'))
        outlet.category = accessory.Category.OUTLET  # Test another Category besides OTHER
        acc_pattern = 'X-HM://00145Q53I' + acc.setup_id
        outlet_pattern = 'X-HM://0061QIA1A' + outlet.setup_id
        assert (acc.xhm_uri == acc_pattern
                and outlet.xhm_uri == outlet_pattern)


class TestBridge(TestAccessory):

    def test_init(self):
        bridge = accessory.Bridge("Test Bridge")
        assert bridge.category == accessory.Category.BRIDGE

    def test_add_accessory(self):
        bridge = accessory.Bridge("Test Bridge")
        acc = accessory.Accessory("Test Accessory", aid=2)
        bridge.add_accessory(acc)
        acc2 = accessory.Accessory("Test Accessory 2")
        bridge.add_accessory(acc2)
        assert (acc2.aid != accessory.STANDALONE_AID
                and acc2.aid != acc.aid)

    def test_n_add_accessory_bridge_aid(self):
        bridge = accessory.Bridge("Test Bridge")
        acc = accessory.Accessory("Test Accessory", aid=accessory.STANDALONE_AID)
        with pytest.raises(ValueError):
            bridge.add_accessory(acc)

    def test_n_add_accessory_dup_aid(self):
        bridge = accessory.Bridge("Test Bridge")
        acc_1 = accessory.Accessory("Test Accessory 1", aid=2)
        acc_2 = accessory.Accessory("Test Accessory 2", aid=acc_1.aid)
        bridge.add_accessory(acc_1)
        with pytest.raises(ValueError):
            bridge.add_accessory(acc_2)

    def test_n_add_bridge_to_bridge(self):
        bridge = accessory.Bridge('Test Bridge')
        bridge_acc = accessory.Bridge('Test Bridge Acc')
        with pytest.raises(ValueError):
            bridge.add_accessory(bridge_acc)
