"""
Tests for pyhap.tlv
"""
import pytest
import string

import pyhap.tlv as tlv


def test_encode_and_decode():
    test_tag = b'T'
    test_value_short = b'VALUE'
    test_value_long = ((string.ascii_letters + string.digits) * 10).encode()
    x = tlv.encode(test_tag, test_value_short)
    y = tlv.encode(test_tag, test_value_long)
    x_decoded = tlv.decode(x)
    y_decoded = tlv.decode(y)
    assert (x_decoded[b'T'] == test_value_short
            and y_decoded[b'T'] == test_value_long)
