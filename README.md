## API Insee

Python helper to request Sirene API

API Sirene give access to French companies and business database. Entities are recorded since the creation
of this administrative register in 1973. To use this API you have to create an account on <https://api.insee.fr/>

You will find the official documentation [here](https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=Sirene&version=V3&provider=insee). All examples described here comes from the official documentation.


#### Installation

You can install the helper with pip

```
pip install api-insee
```

To use the api within a python script

```python
from api_insee import ApiInsee

api = ApiInsee(
    key = # your consumer key,
    secret = # your consumer secret
)

```

#### Siren and Siret service

To get information about a siren number

```python
data = api.siren('005520135').get()
```

This simple code call ```https://api.insee.fr/entreprises/sirene/V3/siren/005520135``` and return these data :

```json
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
```

The same logic for a siret number

```python
data = api.siret('39860733300059').get()
# call https://api.insee.fr/entreprises/sirene/V3/siret/39860733300059
```

#### Request Params

To pass url params to your request use keyword argument

```python
data = api.siren('005520135', date='2018-01-01').get()
# https://api.insee.fr/entreprises/sirene/V3/siren/005520135?date=2018-01-01
```

#### Multicriteria search

Sirene API let you search entities using 'q' url parameter. For example
to get all siren entities with ```codeCommuneEtablissement``` egal to ```92046``` you can do this request

```python
data = api.siren(q='unitePurgeeUniteLegage:True').get()
```

```api_insee``` comes with ```Criteria``` to help you to write theses requests.

```python
import api_insee.criteria as Criteria
```

##### Criteria.Field

search on a specific field

```python
data = api.siren(q=Criteria.Field('unitePurgeeUniteLegale', True)).get()

# will search on all entities with unitePurgeeUniteLeage=True
# /?q=unitePurgeeUniteLegale:True
```

you can combine several criteria together. By default the ```AND``` operator
is used between each criteria.

```python

data = api.siren(q=(
    Critera.Field('codeCommuneEtablissement', 92046),
    Criteria.Field('unitePurgeeUniteLegale', True)
)).get()

# /?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True

```

or you can use a dictionnary to search on multiple fields

```python

data = api.siren(q={
    'codeCommuneEtablissement' : 92046,
    'unitePurgeeUniteLegale' : True
}).get()

# /?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True

```

You can use ```|``` and ```&``` logical operator to specify your requests

```python
data = api.siren(q=(
    Criteria.Field('codeCommuneEtablissement', 92046) | Criterial.Field('unitePurgeeUniteLegale', True)
)).get()

# /?q=codeCommuneEtablissement:92046 OR unitePurgeeUniteLegale:True
```

```-``` is used as ```NOT``` operator

```python
data = api.siren(q=-Criteria.Field('codeCommuneEtablissement', 92046)).get()

# /?q=-codeCommuneEtablissement:92046
```

##### Criteria.FieldExact

To search a field on an exact value

```python
data = api.siren(q=Criteria.FieldExact('demoninationUniteLegale','LE TIMBRE')).get()
# /?q=demoninationUniteLegale:"LE TIMBRE"
```

##### Criteria.Periodic

Periodic Field can be search with ```Criteria.Periodic```

```python

data = api.siren(q= Criteria.Periodic(
    Criteria.Field('activitePrincipaleUniteLegale','84.23Z') |
    Criteria.Field('activitePrincipaleUniteLegale','86.21Z')
)).get()

# /?q=periode(activitePrincipaleUniteLegale:84.23Z OR activitePrincipaleUniteLegale:86.21Z)
```

##### Criteria.Range

to search on a specific range of values

```python
data = api.siren(q=Criteria.Range('nomUsageUniteLegale', 'DUPONT', 'DURANT'))
# /?q=nomUsageUniteLegale:[DUPONT TO DURANT]

data = api.siren(q=Criteria.Range('nomUsageUniteLegale', 'DUPONT', 'DURANT', exclude=True))
# /?q=nomUsageUniteLegale:%7BDUPONT TO DURANT%7D
```

#### Pagination

To specify the number of results per page use the ```nombre``` argument. The ```pages()``` method return an iterator
to let you fetch pages from the api.

```python
from api_insee import ApiInsee

api = ApiInsee(
    key = 'YOUR-KEY',
    secret = 'YOUR-SECRET
)

request = api.siren(q={
    'categorieEntreprise': 'PME'
}, nombre= 100)

for (page_index, page_result) in enumerate(request.pages()):
    # process page_result
