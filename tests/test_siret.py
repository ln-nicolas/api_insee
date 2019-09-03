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

def test_siret_search(execute_request):

    request = api.siret('39860733300059')
    unit    = request.get()

    assert unit['etablissement']['siret'] == '39860733300059'
    assert unit['header']['statut'] == 200
    assert request.url == base_siret_url + '/39860733300059'

    execute_request(request)

def test_siret_search_with_date(execute_request):

    request = api.siret('39860733300059', date='2015-08-01')
    assert request.url == base_siret_url + '/39860733300059?date=2015-08-01'

    execute_request(request)

def test_siret_search_with_champs(execute_request):

    champs = [
        'siret',
        'denominationUniteLegale',
        'nomUsageUniteLegale',
        'prenom1UniteLegale',
    ]

    request = api.siret('39860733300059', champs=champs)
    assert request.url == base_siret_url + '/39860733300059?champs=siret,denominationUniteLegale,nomUsageUniteLegale,prenom1UniteLegale'

    execute_request(request)


def test_siret_search_with_2_criteria(execute_request):

    request = api.siret(
        q = (Criteria.Field('codeCommuneEtablissement', 92046),
        Criteria.Field('unitePurgeeUniteLegale', True))
    )

    assert request.url == base_siret_url + '?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True'

    execute_request(request)

def test_siret_search_with_2_criteria_and_date(execute_request):

    request = api.siret(
        q = (Criteria.Field('codeCommuneEtablissement', 92046),
        Criteria.Field('unitePurgeeUniteLegale', True)),
        date='2018-01-01'
    )

    assert request.url == base_siret_url + '?date=2018-01-01&q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True'

    execute_request(request)


def test_siret_search_from_dic_criteria(execute_request):

    request = api.siret(q={
        'unitePurgeeUniteLegale' : True,
        'codeCommuneEtablissement' : 92046
    })

    assert (
        request.url == base_siret_url + '?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True'\
        or request.url == base_siret_url + '?q=unitePurgeeUniteLegale:True AND codeCommuneEtablissement:92046'
    )

    execute_request(request)

def test_siret_search_with_operators_or_and_parentheses(execute_request):

    request = api.siret(q=(
        (Criteria.Field('codeCommuneEtablissement', 92046) | Criteria.Field('unitePurgeeUniteLegale', True)) &
         Criteria.Field('codeCommuneEtablissement', 92046)
    ))

    assert (
        request.url == base_siret_url + '?q=codeCommuneEtablissement:92046 OR unitePurgeeUniteLegale:True AND codeCommuneEtablissement:92046'
    )

    execute_request(request)


def test_siret_search_with_operators(execute_request):

    request = api.siret(q=Criteria.Field('codeCommuneEtablissement', 92046) | Criteria.Field('unitePurgeeUniteLegale', True))

    assert (
        request.url == base_siret_url + '?q=codeCommuneEtablissement:92046 OR unitePurgeeUniteLegale:True'
    )

    execute_request(request)


def test_siret_search_with_not_operator(execute_request):

    request = api.siret(
        q=(-(-Criteria.Field('codeCommuneEtablissement', 92046)),
        -Criteria.Field('unitePurgeeUniteLegale', True))
    )

    assert request.url == base_siret_url + '?q=codeCommuneEtablissement:92046 AND -unitePurgeeUniteLegale:True'

    execute_request(request)

def test_siret_search_with_periodic_list(execute_request):

    request = api.siret(
        q=Criteria.Periodic(
            Criteria.Field('activitePrincipaleEtablissement','84.23Z'),
            Criteria.Field('etatAdministratifEtablissement','A')
        )
    )
    assert request.url == base_siret_url + '?q=periode(activitePrincipaleEtablissement:84.23Z AND etatAdministratifEtablissement:A)'

    execute_request(request)

def test_siret_search_with_periodic_list_with_or(execute_request):

    request = api.siret(
        q=Criteria.Periodic(
            Criteria.Field('activitePrincipaleEtablissement','84.23Z'),
            Criteria.Field('activitePrincipaleEtablissement','86.21Z'),
            Criteria.Field('activitePrincipaleEtablissement','87.21Z'),
            operator = 'OR'
        )
    )

    assert request.url == base_siret_url + '?q=periode(activitePrincipaleEtablissement:84.23Z OR activitePrincipaleEtablissement:86.21Z OR activitePrincipaleEtablissement:87.21Z)'

    execute_request(request)

def test_siret_search_with_periodic_list_and_operators(execute_request):

    request = api.siret(
        q=Criteria.Periodic(
            Criteria.Field('activitePrincipaleEtablissement','84.23Z') |
            Criteria.Field('activitePrincipaleEtablissement','86.21Z') &
            Criteria.Field('etatAdministratifEtablissement','A')
        )
    )

    assert request.url == base_siret_url + '?q=periode(activitePrincipaleEtablissement:84.23Z OR activitePrincipaleEtablissement:86.21Z AND etatAdministratifEtablissement:A)'

    execute_request(request)

def test_siret_search_with_periodic_list_and_operators_excluding(execute_request):

    request = api.siret(
        q= Criteria.Periodic(
            Criteria.Field('activitePrincipaleEtablissement','84.23Z') |
            Criteria.Field('activitePrincipaleEtablissement','86.21Z')
        ) &
        Criteria.PeriodicField('etatAdministratifEtablissement','A')
    )

    assert request.url == base_siret_url + '?q=periode(activitePrincipaleEtablissement:84.23Z OR activitePrincipaleEtablissement:86.21Z) AND periode(etatAdministratifEtablissement:A)'

    execute_request(request)


def test_siret_search_with_including_borne(execute_request):

    request = api.siret(
        q=Criteria.Range('nomUsageUniteLegale', 'DUPONT', 'DURANT')
    )

    assert request.url == base_siret_url + '?q=nomUsageUniteLegale:[DUPONT TO DURANT]'

    execute_request(request)

def test_siret_search_with_excluding_borne(execute_request):

    request = api.siret(
        q=Criteria.Range('nomUsageUniteLegale', 'DUPONT', 'DURANT', exclude=True)
    )

    assert request.url == base_siret_url + '?q=nomUsageUniteLegale:{DUPONT TO DURANT}'

    execute_request(request)
