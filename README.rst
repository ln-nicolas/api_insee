API Insee
---------

Python helper to request Sirene API

API Sirene give access to French companies and business database.
Entities are recorded since the creation of this administrative register
in 1973. To use this API you have to create an account on
https://api.insee.fr/

You will find the official documentation
`here <https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=Sirene&version=V3&provider=insee>`__.
All examples described here comes from the official documentation.

Installation
^^^^^^^^^^^^

You can install the helper with pip

::

    pip install api-insee

To use the api within a python script

.. code:: python

    from api_insee import ApiInsee

    api = ApiInsee(
        key = # your consumer key,
        secret = # your consumer secret
    )

Siren and Siret service
^^^^^^^^^^^^^^^^^^^^^^^

To get information about a siren number

.. code:: python

    data = api.siren('005520135').get()

This simple code call
``https://api.insee.fr/entreprises/sirene/V3/siren/005520135`` and
return these data :

.. code:: json

    {
      "header": {
        "statut": 200,
        "message": "OK"
      },
      "uniteLegale": {
        "siren": "005520135",
        ...
        "periodesUniteLegale": [
          {
            "dateFin": null,
            "dateDebut": "2007-11-19",
            "etatAdministratifUniteLegale": "C",
            "changementEtatAdministratifUniteLegale": true,
            "nomUniteLegale": null,
            ...
          }
          ...
        ]
      }
    }

The same logic for a siret number

.. code:: python

    data = api.siret('39860733300059').get()
    # call https://api.insee.fr/entreprises/sirene/V3/siret/39860733300059

Request Params
^^^^^^^^^^^^^^

To pass url params to your request use keyword argument

.. code:: python

    data = api.siren('005520135', date='2018-01-01').get()
    # https://api.insee.fr/entreprises/sirene/V3/siren/005520135?date=2018-01-01

Multicriteria search
^^^^^^^^^^^^^^^^^^^^

Sirene API let you search entities using 'q' url parameter. For example
to get all siren entities with ``codeCommuneEtablissement`` egal to
``92046`` you can do this request

.. code:: python

    data = api.siren(q='unitePurgeeUniteLegage:True').get()

``api_insee`` comes with ``Criteria`` to help you to write theses
requests.

.. code:: python

    import api_insee.criteria as Criteria

Criteria.Field
''''''''''''''

search on a specific field

.. code:: python

    data = api.siren(q=Criteria.Field('unitePurgeeUniteLegale', True)).get()

    # will search on all entities with unitePurgeeUniteLeage=True
    # /?q=unitePurgeeUniteLegale:True

you can combine several criteria together. By default the ``AND``
operator is used between each criteria.

.. code:: python


    data = api.siren(q=(
        Critera.Field('codeCommuneEtablissement', 92046),
        Criteria.Field('unitePurgeeUniteLegale', True)
    )).get()

    # /?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True

or you can use a dictionnary to search on multiple fields

.. code:: python


    data = api.siren(q={
        'codeCommuneEtablissement' : 92046,
        'unitePurgeeUniteLegale' : True
    }).get()

    # /?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True

You can use ``|`` and ``&`` logical operator to specify your requests

.. code:: python

    data = api.siren(q=(
        Criteria.Field('codeCommuneEtablissement', 92046) | Criterial.Field('unitePurgeeUniteLegale', True)
    )).get()

    # /?q=codeCommuneEtablissement:92046 OR unitePurgeeUniteLegale:True

``-`` is used as ``NOT`` operator

.. code:: python

    data = api.siren(q=-Criteria.Field('codeCommuneEtablissement', 92046)).get()

    # /?q=-codeCommuneEtablissement:92046

Criteria.FieldExact
'''''''''''''''''''

To search a field on an exact value

.. code:: python

    data = api.siren(q=Criteria.FieldExact('demoninationUniteLegale','LE TIMBRE')).get()
    # /?q=demoninationUniteLegale:"LE TIMBRE"

Criteria.Periodic
'''''''''''''''''

Periodic Field can be search with ``Criteria.Periodic``

.. code:: python


    data = api.siren(q= Criteria.Periodic(
        Criteria.Field('activitePrincipaleUniteLegale','84.23Z') |
        Criteria.Field('activitePrincipaleUniteLegale','86.21Z')
    )).get()

    # /?q=periode(activitePrincipaleUniteLegale:84.23Z OR activitePrincipaleUniteLegale:86.21Z)

Criteria.Range
''''''''''''''

to search on a specific range of values

.. code:: python

    data = api.siren(q=Criteria.Range('nomUsageUniteLegale', 'DUPONT', 'DURANT'))
    # /?q=nomUsageUniteLegale:[DUPONT TO DURANT]

    data = api.siren(q=Criteria.Range('nomUsageUniteLegale', 'DUPONT', 'DURANT', exclude=True))
    # /?q=nomUsageUniteLegale:%7BDUPONT TO DURANT%7D

Pagination
^^^^^^^^^^

The ``pages()`` method return an iterator to let you fetch pages from
the api. To specify the number of results per page use the ``nombre``
argument. Results are limited by 10000 per pages.

\`\`\`python from api\_insee import ApiInsee

api = ApiInsee( key = 'YOUR-KEY', secret = 'YOUR-SECRET )

request = api.siren(q={ 'categorieEntreprise': 'PME' })

for (page\_index, page\_result) in
enumerate(request.pages(nombre=1000)): # process page\_result
