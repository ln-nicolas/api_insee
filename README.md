**[🇺🇸 English -> ](https://github.com/sne3ks/api_insee/blob/master/README.fr.md)**

API Sirene donne accès aux informations concernant les entreprises et les établissements immatriculés au répertoire interadministratif Sirene depuis sa création en 1973, y compris les unités fermées. La recherche peut être unitaire, multicritère, phonétique et porter sur les données courantes et historisées. Les services actuellement disponibles interrogent les unités légales (Siren) et les établissements (Siret).

La bibliothéque python ```api_insee``` est une aide pour d'interroger l'API Sirene en toute simplicité.
Vous trouverez d'avantage d'informations au sujet de l'API Sirene dans la [documentation officielle](https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/item-info.jag?name=Sirene&version=V3&provider=insee)


#### Installation

Depuis un terminal :

`pip install api-insee`

Pour pouvoir interroger l'api vous devez créer un compte consommateur sur [api.insee.fr](https://api.insee.fr).
Puis récupérer vos clés consommateur et secrète.

```python
from api_insee import ApiInsee

api = ApiInsee(
    key = # clé consommateur,
    secret = # clé secrète
)
```
---------------------------

#### Exemples d'interrogation

* Récupérer les informations à partir d'un numéro sirene ou siret

```python
data = api.siren('005520135').get()
data = api.siret('39860733300059').get()


# Requêtes envoyées:
# https://api.insee.fr/entreprises/sirene/V3/siren/005520135
# https://api.insee.fr/entreprises/sirene/V3/siret/39860733300059
```

* Passer des paramètres à la requête

```python
data = api.siren('005520135', date='2018-01-01').get()

# Requête envoyées:
# https://api.insee.fr/entreprises/sirene/V3/siren/005520135?date=2018-01-01
```

* Faire une recherche avancée sur des critères donnés, en utilisant le paramètre ```q=```

```python
data = api.siren(q='unitePurgeeUniteLegage:True').get()
```
--------------------------------

#### Recherches avancées sur critéres

Les classes ```api_insee.criteria``` permettent de construire
les requêtes de recherche avancées plus facilement. Vous trouverez dans [la documentation officielle](https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/templates/api/documentation/download.jag?tenant=carbon.super&resourceUrl=/registry/resource/_system/governance/apimgt/applicationdata/provider/insee/Sirene/V3/documentation/files/INSEE%20Documentation%20API%20Sirene%20Variables-V3.7.pdf) l'ensemble des variables disponibles.

* Vous pouvez par exemple combiner plusieurs critères sur une seule
requête.

```python
from api_insee.criteria import Field

data = api.siren(q=(
    Field('codeCommuneEtablissement', 92046),
    Field('unitePurgeeUniteLegale', True)
)).get()


# Requête envoyée:
# /?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True
```

* Ou encore en utilisant un dictionnaire

```python

data = api.siren(q={
    'codeCommuneEtablissement' : 92046,
    'unitePurgeeUniteLegale' : True
}).get()


# Requête envoyée:
# /?q=codeCommuneEtablissement:92046 AND unitePurgeeUniteLegale:True

```

* Utilisez les opérateurs logiques ```|```, ```&```, ```- (not)``` pour préciser vos requêtes.

```python

data = api.siren(q=(
    Field('codeCommuneEtablissement', 92046) | Field('unitePurgeeUniteLegale', True)
)).get()

data = api.siren(q=-Field('codeCommuneEtablissement', 92046)).get()

# Requêtes envoyées:
# /?q=codeCommuneEtablissement:92046 OR unitePurgeeUniteLegale:True
# /?q=-codeCommuneEtablissement:92046
```

* Filtrer les champs retournés par la réponse

```python
champs = [
    'siret',
    'denominationUniteLegale',
    'nomUsageUniteLegale',
    'prenom1UniteLegale',
]

request = api.siret('39860733300059', champs=champs)
# Request executed:
# /39860733300059?champs=siret,denominationUniteLegale,nomUsageUniteLegale,prenom1UniteLegale
```

##### Recherche multicritère liens de succession

* Interroger le service des liens de succession. (Uniquement disponible depuis la version 1.5 de api_insee)

```python

request = api.liens_succession(q=Criteria.Field('siretEtablissementPredecesseur', 39860733300042))
# '/liensSuccession?q=siretEtablissementPredecesseur:39860733300042'

request = api.liens_succession(q=(
    Criteria.Field('siretEtablissementPredecesseur', '00555008200027') &
    Criteria.Field('dateLienSuccession', '2004-04-01')
))
# '/liensSuccession?q=siretEtablissementPredecesseur:00555008200027 AND dateLienSuccession:2004-04-01'
```

##### Recherches spéciales

|Type|Description|Exemple|
|----|-----------|-------|
|FieldExact| Recherche la valeur exact|FieldExact('demoninationUniteLegale','LE TIMBRE'))|
|Periodic| Recherche sur un champ périodique|Periodic(Field('activitePrincipaleUniteLegale','84.23Z') | Field('activitePrincipaleUniteLegale','86.21Z')))|
|Range| Recherche sur un interval|Range('nomUsageUniteLegale', 'DUPONT', 'DURANT')|

----------------


#### Pagination

Pour les requêtes retournant beaucoup de résultats, il est possible de parcourir les résultats grâce à la méthode ```pages()```. Le paramètre ```nombre``` spécifie le nombre de résultats par pages. La limite définie par l'insee est 1000 résultats par pages.

```python
from api_insee import ApiInsee

api = ApiInsee(
    key = # clé consommateur,
    secret = # clé secrète
)

request = api.siren(q={
    'categorieEntreprise': 'PME'
})

for (page_index, page_result) in enumerate(request.pages(nombre=1000)):
    # votre code ici ..
```
