"""
Tests for pyhap.util
"""
import pytest

import pyhap.util as util


def test_long_to_bytes():
    long_int = 999999
    x = util.long_to_bytes(long_int)
    assert x.decode() == '\x0fB?'
