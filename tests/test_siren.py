#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import conftest as conf

from api_insee import ApiInsee
from api_insee.conf import API_VERSION
import api_insee.criteria as Criteria

#from api_insee.exeptions.params_exeption import ParamsExeptions

__author__ = "Lenselle Nicolas"
__copyright__ = "Lenselle Nicolas"
__license__ = "mit"

api = ApiInsee(
    key = conf.SIRENE_API_CONSUMER_KEY,
    secret = conf.SIRENE_API_CONSUMER_SECRET
)

base_siren_url = API_VERSION['url'] + API_VERSION['path_siren']

def test_siren_search():

    request = api.siren('809893225')
    unit    = request.get()

    assert unit['uniteLegale']['siren'] == '809893225'
    assert unit['header']['statut'] == 200
    assert request.url == base_siren_url + '/809893225/'

def test_siren_raw_search():

    criteria = Criteria.Raw('unitePurgeeUniteLegale:True')
    request  = api.siren(q=criteria)
    results  = request.get()

    assert results['header']['statut'] == 200
    assert request.url == base_siren_url + '/?q=unitePurgeeUniteLegale:True'


def test_siren_search_by_field():

    criteria = Criteria.Field('unitePurgeeUniteLegale',True)
    request  = api.siren(q=criteria)
    results  = request.get()

    assert results['header']['statut'] == 200
    assert request.url == base_siren_url + '/?q=unitePurgeeUniteLegale:True'


def test_siren_search_date():

    request = api.siren('005520135', date='2018-01-01')

    assert request.url == base_siren_url + '/005520135/?date=2018-01-01'

def test_siren_search_with_2_criteria():

    request = api.siren(
        q = (Criteria.Field('codeCommuneEtablissement', 92046),
        Criteria.Field('unitePurgeeUniteLegale', True))
    )

    assert request.url == base_siren_url + '/?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True'

def test_siren_search_with_2_criteria_and_date():
    request = api.siren(
        q = (Criteria.Field('codeCommuneEtablissement', 92046),
        Criteria.Field('unitePurgeeUniteLegale', True)),
        date='2018-01-01'
    )

    assert request.url == base_siren_url + '/?date=2018-01-01&q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True'



def test_siren_search_from_dic_criteria():

    request = api.siren(q={
        'unitePurgeeUniteLegale' : True,
        'codeCommuneEtablissement' : 92046
    })

    assert (
        request.url == base_siren_url + '/?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True'\
        or request.url == base_siren_url + '/?q=unitePurgeeUniteLegale:True AND codeCommuneEtablissement:92046'
    )

def test_siren_search_with_period_variable():

    request = api.siren(
        q=Criteria.PeriodicField('etatAdministratifUniteLegale','C')
    )

    assert request.url == base_siren_url + '/?q=periode(etatAdministratifUniteLegale:C)'

def test_siren_search_with_not_operator():

    request = api.siren(
        q=(-(-Criteria.Field('codeCommuneEtablissement', 92046)),
        -Criteria.Field('unitePurgeeUniteLegale', True))
    )

    assert request.url == base_siren_url + '/?q=codeCommuneEtablissement:92046 AND -unitePurgeeUniteLegale:True'

def test_siren_search_with_periodic_list():

    request = api.siren(
        q=Criteria.Periodic(
            Criteria.Field('activitePrincipaleUniteLegale','84.23Z'),
            Criteria.Field('activitePrincipaleUniteLegale','86.21Z')
        )
    )

    assert request.url == base_siren_url + '/?q=periode(activitePrincipaleUniteLegale:84.23Z AND activitePrincipaleUniteLegale:86.21Z)'

def test_siren_search_with_periodic_list_with_or():

    request = api.siren(
        q=Criteria.Periodic(
            Criteria.Field('activitePrincipaleUniteLegale','84.23Z'),
            Criteria.Field('activitePrincipaleUniteLegale','86.21Z'),
            Criteria.Field('activitePrincipaleUniteLegale','87.21Z'),
            operator = 'OR'
        )
    )

    assert request.url == base_siren_url + '/?q=periode(activitePrincipaleUniteLegale:84.23Z OR activitePrincipaleUniteLegale:86.21Z OR activitePrincipaleUniteLegale:87.21Z)'


def test_siren_search_with_periodic_list_and_operators():

    request = api.siren(
        q=Criteria.Periodic(
            Criteria.Field('activitePrincipaleUniteLegale','84.23Z') |
            Criteria.Field('activitePrincipaleUniteLegale','86.21Z') &
            Criteria.Field('activitePrincipaleUniteLegale','87.21Z')
        )
    )

    assert request.url == base_siren_url + '/?q=periode(activitePrincipaleUniteLegale:84.23Z OR activitePrincipaleUniteLegale:86.21Z AND activitePrincipaleUniteLegale:87.21Z)'

def test_siren_search_with_periodic_list_and_operators_excluding():

    request = api.siren(
        q= Criteria.Periodic(
            Criteria.Field('activitePrincipaleUniteLegale','84.23Z') |
            Criteria.Field('activitePrincipaleUniteLegale','86.21Z')
        ) &
        Criteria.PeriodicField('activitePrincipaleUniteLegale','87.21Z')
    )

    assert request.url == base_siren_url + '/?q=periode(activitePrincipaleUniteLegale:84.23Z OR activitePrincipaleUniteLegale:86.21Z) AND periode(activitePrincipaleUniteLegale:87.21Z)'


def test_siren_search_exact_field():

    request = api.siren(
        q=Criteria.Periodic(Criteria.FieldExact('denominationUniteLegale','LE TIMBRE'))
    )

    assert request.url == base_siren_url + '/?q=periode(denominationUniteLegale:"LE TIMBRE")'

def test_siren_search_with_including_borne():

    request = api.siren(
        q=Criteria.Range('nomUsageUniteLegale', 'DUPONT', 'DURANT')
    )

    assert request.url == base_siren_url + '/?q=nomUsageUniteLegale:[DUPONT TO DURANT]'

def test_siren_search_with_excluding_borne():

    request = api.siren(
        q=Criteria.Range('nomUsageUniteLegale', 'DUPONT', 'DURANT', exclude=True)
    )

    assert request.url == base_siren_url + '/?q=nomUsageUniteLegale:%7BDUPONT TO DURANT%7D'
