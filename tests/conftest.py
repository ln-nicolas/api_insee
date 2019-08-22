#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

"""
    Replace API consumer data with yours
"""
SIRENE_API_CONSUMER_KEY    = 'DFUozAz4vYtwhEFfbSmx8mvavzsa'
SIRENE_API_CONSUMER_SECRET = 'nB_0Cv7nzCs3_FeEtr0D_jObttMa'
SIRENE_API_TOKEN           = 'b42db1ef-4b19-3818-a6e0-82f7eed776fe'

def pytest_addoption(parser):
    parser.addoption(
        "--api-insee-execute-request", 
        action="store", 
        default=False, 
        help="Execute api request"
    )

@pytest.fixture
def execute_request(request):
    
    def exec(api_request):
        if request.config.getoption("--api-insee-execute-request"):
            api_request.get()

    return exec