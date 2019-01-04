## API Insee

Python helper to request Sirene API

API Sirene give access to French companies and business database. Entities are recorded since the creation
of this administrative register in 1973. To use this API you have to create an account on <https://api.insee.fr/>

You will find the official documentation [here](https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=Sirene&version=V3&provider=insee). All examples described here comes from the official documentation.


#### Installation

You can install the helper with pip

```
pip install api_insee
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
