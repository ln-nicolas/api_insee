#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import conftest as conf

from api_insee import ApiInsee
from api_insee.conf import API_VERSION
import api_insee.criteria as Criteria

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"

api = ApiInsee(
    key = conf.SIRENE_API_CONSUMER_KEY,
    secret = conf.SIRENE_API_CONSUMER_SECRET
)

base_siret_url = API_VERSION['url'] + API_VERSION['path_siret']

def test_siret_search():

    request = api.siret('39860733300059')
    unit    = request.get()

    assert unit['etablissement']['siret'] == '39860733300059'
    assert unit['header']['statut'] == 200
    assert request.url == base_siret_url + '/39860733300059/'

def test_siret_search_with_date():

    request = api.siret('39860733300059', date='2015-08-01')
    assert request.url == base_siret_url + '/39860733300059/?date=2015-08-01'
