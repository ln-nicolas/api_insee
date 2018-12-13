#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from api_insee.skeleton import fib

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
