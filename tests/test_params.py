"""
Tests for pyhap.util
"""
import pytest
import hashlib

import pyhap.params as params


def test_srp_ctx():
    n_len = 1024
    hashfunc = hashlib.sha512
    salt_len = 16
    ctx = params.get_srp_context(n_len, hashfunc, salt_len)
    print(ctx['g'], flush=True)
    assert (ctx['hashfunc'] == hashfunc
            and ctx['N'] == 167609434410335061345139523764350090260135525329813904557420930309800865859473551531551523800013916573891864789934747039010546328480848979516637673776605610374669426214776197828492691384519453218253702788022233205683635831626913357154941914129985489522629902540768368409482248290641036967659389658897350067939
            and ctx['g'] == 2
            and ctx['N_len'] == n_len
            and ctx['salt_len'] == salt_len)
