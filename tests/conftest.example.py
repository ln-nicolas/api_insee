#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import os
import sys
import importlib.util


#
#  Import API Insee Module 
# 

dir_path = os.path.dirname(os.path.realpath(__file__))
MODULE_PATH = dir_path+"/../src/api_insee/__init__.py"
MODULE_NAME = "api_insee"
spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


#
#  Replace API consumer data with yours
#

SIRENE_API_CONSUMER_KEY    = "your-key"
SIRENE_API_CONSUMER_SECRET = "your-secret"
SIRENE_API_TOKEN           = "your-token"


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