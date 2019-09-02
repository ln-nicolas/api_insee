Python helper to request Sirene API \*\* `🇫🇷
Français <https://github.com/sne3ks/api_insee/blob/master/README.fr.md>`__
\*\*

API Sirene give access to French companies and business database.
Entities are recorded since the creation of this administrative register
in 1973. To use this API you have to create an account on
https://api.insee.fr/

The python library ``api_insee`` is a help to request the API Sirene in
perfect simplicity. You'll find more information about the API in the
`official
documentation <https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=Sirene&version=V3&provider=insee>`__

Installation
^^^^^^^^^^^^

From a terminal :

``pip install api-insee``

To request the API you must create a consummer account on
`api.insee.fr <https://api.insee.fr>`__. Then with your access keys :

.. code:: python

    from api_insee import ApiInsee

    api = ApiInsee(
        key = # consummer key,
        secret = # secret key
    )

--------------

Request samples
^^^^^^^^^^^^^^^

-  Fetch data from a siret or sirene number

.. code:: python

    data = api.siren('005520135').get()
    data = api.siret('39860733300059').get()


    # Request executed:
    # https://api.insee.fr/entreprises/sirene/V3/siren/005520135
    # https://api.insee.fr/entreprises/sirene/V3/siret/39860733300059

-  Set parameters to the request:

.. code:: python

    data = api.siren('005520135', date='2018-01-01').get()

    # Request executed:
    # https://api.insee.fr/entreprises/sirene/V3/siren/005520135?date=2018-01-01

-  Perform an advanced search on given criteria using ``q=`` parameter

.. code:: python

    data = api.siren(q='unitePurgeeUniteLegage:True').get()

    # Request executed:
    # /?q=unitePurgeeUniteLegage:True

--------------

Advanced search on criteria
'''''''''''''''''''''''''''

Class in ``api_insee.criteria`` let you construct advanced searchs
easily. All variables available are described in the `official
documentation <https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/templates/api/documentation/download.jag?tenant=carbon.super&resourceUrl=/registry/resource/_system/governance/apimgt/applicationdata/provider/insee/Sirene/V3/documentation/files/INSEE%20Documentation%20API%20Sirene%20Variables-V3.7.pdf>`__

-  You can combine several criteria in one request.

.. code:: python

    from api_insee.criteria import Field

    data = api.siren(q=(
        Field('codeCommuneEtablissement', 92046),
        Field('unitePurgeeUniteLegale', True)
    )).get()


    # Request executed:
    # /?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True

-  Or using a dictionnary

.. code:: python


    data = api.siren(q={
        'codeCommuneEtablissement' : 92046,
        'unitePurgeeUniteLegale' : True
    }).get()


    # Request executed:
    # /?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True

-  Use logical operator ``|``, ``&``, ``- (not)`` to specify your
   requests.

.. code:: python


    data = api.siren(q=(
        Field('codeCommuneEtablissement', 92046) | Field('unitePurgeeUniteLegale', True)
    )).get()

    data = api.siren(q=-Field('codeCommuneEtablissement', 92046)).get()

    # Request executed:
    # /?q=codeCommuneEtablissement:92046 OR unitePurgeeUniteLegale:True

Special Search
''''''''''''''

+-------+--------------+----------+
| Type  | Description  | Example  |
+=======+==============+==========+
| Field | Search on an | ``FieldE |
| Exact | exact value  | xact('de |
|       |              | moninati |
|       |              | onUniteL |
|       |              | egale',' |
|       |              | LE TIMBR |
|       |              | E'))``   |
+-------+--------------+----------+
| Perio | Search on    | ``Period |
| dic   | periodic     | ic(Field |
|       | field        | ('activi |
|       |              | tePrinci |
|       |              | paleUnit |
|       |              | eLegale' |
|       |              | ,'84.23Z |
|       |              | ') | Fie |
|       |              | ld('acti |
|       |              | vitePrin |
|       |              | cipaleUn |
|       |              | iteLegal |
|       |              | e','86.2 |
|       |              | 1Z')))`` |
+-------+--------------+----------+
| Range | Search in a  | ``Range( |
|       | range of     | 'nomUsag |
|       | values       | eUniteLe |
|       |              | gale', ' |
|       |              | DUPONT', |
|       |              |  'DURANT |
|       |              | ')``     |
+-------+--------------+----------+

--------------

Pagination
^^^^^^^^^^

The ``pages()`` method return an iterator to let you fetch pages from
the api. To specify the number of results per page use the ``nombre``
argument. Results are limited by 10000 per pages.

.. code:: python

    from api_insee import ApiInsee

    api = ApiInsee(
        key = # consummer key,
        secret = # secret key
    )

    request = api.siren(q={
        'categorieEntreprise': 'PME'
    })

    for (page_index, page_result) in enumerate(request.pages(nombre=1000)):
        # process here
