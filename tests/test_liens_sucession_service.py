#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from api_insee import ApiInsee
from api_insee.conf import API_VERSION
import api_insee.criteria as Criteria

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"

base_siret_url = API_VERSION['url'] + API_VERSION['path_siret']


def test_liens_succession_search(api, execute_request):
    request = api.liens_succession(q=Criteria.Field('siretEtablissementPredecesseur', 39860733300042))
    assert request.url == base_siret_url + '/liensSuccession?q=siretEtablissementPredecesseur:39860733300042'

    request = api.liens_succession(q=(
        Criteria.Field('siretEtablissementPredecesseur', '00555008200027') &
        Criteria.Field('dateLienSuccession', '2004-04-01')
    ))
    assert request.url == base_siret_url +  '/liensSuccession?q=siretEtablissementPredecesseur:00555008200027 AND dateLienSuccession:2004-04-01'

@pytest.mark.http
def test_liens_succession_search_request(api, execute_request):

    request = api.liens_succession(q=Criteria.Field('siretEtablissementPredecesseur', 39860733300042))
    data = request.get()
    assert data['liensSuccession'][0]['siretEtablissementPredecesseur'] == '39860733300042'

    request = api.liens_succession(q=(
        Criteria.Field('siretEtablissementPredecesseur', '00555008200027') &
        Criteria.Field('dateLienSuccession', '2004-04-01')
    ))
    data = request.get()
    assert data['liensSuccession'][0]['siretEtablissementPredecesseur'] == '00555008200027'
    assert data['liensSuccession'][0]['dateLienSuccession'] == '2004-04-01'