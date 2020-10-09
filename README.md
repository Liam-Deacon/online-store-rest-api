# Online Store Example


<!--lint disable no-inline-padding-->
[![ ](https://img.shields.io/static/v1?label=demo&message=REST%20API&color=darkorchid&logo=Heroku&logoColor=white)](https://online-store-flask-rest-api.herokuapp.com/apidocs/)
[![ ](https://img.shields.io/static/v1?label=docs&message=GitHub%20Pages&color=orange&logo=Read%20The%20Docs&logoColor=white)](https://liam-deacon.github.io/online-store-rest-api/)
[[![GitHub pull-requests closed](https://img.shields.io/github/issues-pr-closed/liam-deacon/online-store-rest-api.svg)](https://GitHub.com/liam-deacon/online-store-rest-api/pull/)](https://github.com/Liam-Deacon/online-store-rest-api/pulls)
[![Python CI](https://github.com/Liam-Deacon/online-store-rest-api/workflows/Python%20CI/badge.svg)](https://github.com/Liam-Deacon/online-store-rest-api/actions?query=workflow%3A"Python+CI")
[![Backend Docker CI/CD](https://github.com/Liam-Deacon/online-store-rest-api/workflows/Backend%20Docker%20CI/CD/badge.svg)](https://github.com/Liam-Deacon/online-store-rest-api/actions?query=workflow%3A%22Backend+Docker+CI%2FCD%22)
[![Sphinx Documentation CI](https://github.com/Liam-Deacon/online-store-rest-api/workflows/Sphinx%20Documentation%20CI/badge.svg)](https://github.com/Liam-Deacon/online-store-rest-api/actions?query=workflow%3A%22Sphinx+Documentation+CI%22)
[![ ](https://img.shields.io/pypi/pyversions/metapandas.svg?logo=python)](https://pypi.org/pypi/metapandas/)
[![ ](https://coveralls.io/repos/github/Liam-Deacon/online-store-rest-api/badge.svg?branch=master)](https://coveralls.io/github/Liam-Deacon/online-store-rest-api?branch=master)
[![ ](https://codecov.io/gh/liam-deacon/online-store-rest-api/branch/master/graph/badge.svg)](https://codecov.io/gh/liam-deacon/online-store-rest-api)
[![ ](https://api.codacy.com/project/badge/Grade/de571d98b5ed4203b6eda5f927c8835d)](https://www.codacy.com/gh/liam-deacon/online-store-rest-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=liam-deacon/online-store-rest-api&amp;utm_campaign=Badge_Grade)
[![ ](https://img.shields.io/codefactor/grade/github/liam-deacon/online-store-rest-api?logo=codefactor)](https://www.codefactor.io/repository/github/liam-deacon/online-store-rest-api)
![ ](https://img.shields.io/badge/dev-Open%20in%20Gitpod-blue?logo=gitpod&link=https://gitpod.io/#https://github.com/liam-deacon/online-store-rest-api)
[![ ](https://camo.githubusercontent.com/52feade06f2fecbf006889a904d221e6a730c194/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/github/liam-deacon/online-store-rest-api)
[![ ](https://img.shields.io/badge/Binder%20Launch:-Jupyter%20Lab-blue.svg?colorA=&logo=data:image/png;base64,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)](https://mybinder.org/v2/gh/liam-deacon/online-store-rest-api/master?urlpath=lab)

<!--lint enable no-inline-padding-->

## Background:

This repository was created to solve the [Prezola Technical Challenge](https://github.com/prezola/technical-challenge), which requires a solution capable of adding, removing and listing (added) gifts from a list. It also required a mechanism to purchase a gift from the list and generate a report (of purchased vs non-purchased) gifts.  

This code project takes that concept and extends it to a generic (gift) store.

## The challenge:

_"Write a program to the best of your knowledge which will allow the user to manage a single list of wedding gifts."_

The user must be able to:

- Add a gift to the list
- Remove a gift from the list
- List the already added gifts of the list 
- Purchase a gift from the list
- Generate a report from the list which will print out the gifts and their statuses.
  - The report must include two sections:
    - Purchased gifts: each purchased gift with their details.
    - Not purchased gifts: each available gift with their details.

### Implementation Notes

There are two concrete implementations for realising a gift list with the following classes from `online_store/backend/gift_list.py`:

- `BasicGiftList`, a pure python implementation of a gift list **(Well Tested)**.
- `SqlDatabaseGiftList`, an SQL ORM based implementation of a gift list for use within a flask (or Django) REST API app. In this example, the ORM models are found in `online_store/backend/models/` and the REST API is implemented in `online_store/backend/routes/gifts.py`

### Development Setup ⚙️

```bash
$ npm install  # needed for Swagger JSON to OAS YAML spec conversion
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install setuptools
(venv) $ pip install -r requirements-dev.txt -r requirements-test.txt
(venv) $ pip install -r requirements.txt
```

### Testing 🧪

`setup.cfg` has configured `pytest` to collect coverage information and can be run as follows:

```bash
(venv) $ PYTHONPATH='.' py.test 
```

### Basic Gift List Implementation 🎁

The following showcases a simple python implementation of the gift list:

```python
# load store data
>>> import json
>>> store_items = json.load(open('products.json'))
# import implementation
>>> from online_store.backend.gift_list import BasicGiftList
# create a new gift list
>>> gift_list = BasicGiftList('Liam')
>>> gift_list  # show list representation in interpreter
Liam -> []
# add gift item
>>> gift_list.add_item(store_items[0])
>>> gift_list
Liam -> [{'id': 1, 'name': 'Tea pot', 'brand': 'Le Creuset', 'price': '47.00GBP', 'in_stock_quantity': 50}]
# remove gift item
>>> gift_list.add_item(store_items[1], quantity=3)
>>> gift_list.remove_item(store_items[0])
>>> gift_list
Liam -> [{'id': 2, 'name': 'Cast Iron Oval Casserole - 25cm; Volcanic', 'brand': 'Le Creuset', 'price': '210.00GBP', 'in_stock_quantity': 27}]
# purchase gift item
>>> gift_list.purchase_item(store_items[1], quantity=1)
# generate report
>>> gift_list.create_report()
Gift List Report for Liam:
==============================
Purchased items:
   - {'id': 2, 'name': 'Cast Iron Oval Casserole - 25cm; Volcanic', 'brand': 'Le Creuset', 'price': '210.00GBP', 'in_stock_quantity': 27} (quantity: 1)
------------------------------
Available items:
  - {'id': 2, 'name': 'Cast Iron Oval Casserole - 25cm; Volcanic', 'brand': 'Le Creuset', 'price': '210.00GBP', 'in_stock_quantity': 27} (quantity: 2)
```

### Flask REST API + SQL ORM Implementation 🌍🕸️

Alternatively there is a REST API, which can be run with:

```bash
$ source venv/bin/activate
(venv) $ cd online_store
(venv) $ FLASK_DEBUG=1 flask run
```

This will start a flask development server running on http://localhost:5000 and provides a Swagger-UI at http://localhost:5000/apidocs/. 

#### Examples

```bash
# register a new user
$ curl -X POST -H "Content-Type: application/json" -d '{"username": "me", "password": "test", "email": "me@test.com"}' 'http://localhost:5000/api/v1/auth/register'

{"code":200,"msg":"success","status":"ok"}

# login with user
$ curl -X POST -H "Content-Type: application/json" -d '{"username": "me", "password": "test"}'

{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDIwMTIxMzQsIm5iZiI6MTYwMjAxMjEzNCwianRpIjoiOTA5NTRlZDAtZWIzMy00MTY2LThhODEtZDE5NDI3MjI5NTE0IiwiZXhwIjoxNjAyMDEzMDM0LCJpZGVudGl0eSI6Im1lIiwiZnJlc2giOmZhbHNlLCJ0eXBlIjoiYWNjZXNzIn0.GYVTQK4Xw9JaiJJxa75vlKBS-mho0QjfcM94usPZtSI","code":200,"status":"ok"}

# note access token
$ export TOKEN='<JWT_FROM_LOGIN>'

# access gift list
$ curl -X GET -H  "accept: application/json" -H  "Authorization: Bearer $TOKEN" http://localhost:5000/api/v1/gifts/list

[]

# add one gift item with store id of 1 to list
$ curl -X POST -H  "accept: application/json" -H  "Authorization: Bearer $TOKEN" 'http://localhost:5000/api/v1/gifts/list/add?item_id=1&quantity=1'

{
  "code": 200,
  "msg": "Item added",
  "status": "ok"
}

# remove item with id 1 from gift list
$ curl -X DELETE -H  "accept: application/json" -H  "Authorization: Bearer $TOKEN" http://localhost:5000/api/v1/gifts/list/1

{
  "code": 200,
  "msg": "Item removed",
  "status": "ok"
}

# add then purchase item
$ curl -X POST -H  "accept: application/json" -H  "Authorization: Bearer $TOKEN" 'http://localhost:5000/api/v1/gifts/list/add?item_id=2&quantity=2'

{
  "code": 200,
  "msg": "Item added",
  "status": "ok"
}

$ curl -X POST -H  "accept: application/json" -H  "Authorization: Bearer $TOKEN" http://localhost:5000/api/v1/gifts/list/2/purchase?quantity=1

{
  "code": 200, 
  "msg": "gift purchased", 
  "status": "ok"
}

# produce report
$ curl -X GET -H  "accept: application/json" -H  "Authorization: Bearer $TOKEN" 'http://localhost:5000/api/v1/gifts/list/report'

{
  "available": [
    {
      "brand": "Le Creuset", 
      "currency": "GBP", 
      "id": 2, 
      "in_stock_quantity": 27, 
      "name": "Cast Iron Oval Casserole - 25cm; Volcanic", 
      "price": 210.0, 
      "quantity": 1
    }
  ], 
  "purchased": [
    {
      "brand": "Le Creuset", 
      "currency": "GBP", 
      "id": 2, 
      "in_stock_quantity": 27, 
      "name": "Cast Iron Oval Casserole - 25cm; Volcanic", 
      "price": 210.0, 
      "quantity": 1
    }
  ], 
  "user": 2
}

```

## Bonus Features ✨

There are currently a number of extra features, which help 

- User-friendly backend application logging using `loguru` python package.
- Simple containerisation using Docker - see `DockerFile`
- Authentication using JSON web tokens via [flask-jwt-extended]() middleware.
- [OpenAPI Specification (OAS)](https://swagger.io/specification/) conformant client documentation generated using [flasgger](https://github.com/flasgger/flasgger) and viewable via SwaggerUI [/apidocs](localhost:5000/apidocs) endpoint when running the flask server.
- Persistent data storage using SQL Database modelled using [sqlalchemy](https://docs.sqlalchemy.org/en/13/intro.html) ORM.

### Developer Documentation 📗

The Sphinx documentation builder is currently used to extract python docstrings and the OpenAPI spec of the REST API.

To build the documentation:

```bash
$ cd docs/
$ make openapi_spec.yml
$ make html  # or another end documentation format e.g. epub
```

A live deployment to GitHub Pages can be found at https://liam-deacon.github.io/online-store-rest-api/

## TODO 📝

- [x] Build script / CI using GitHub Actions
- [x] Sphinx documentation support
- [x] Deploy API documentation to GitHub Pages via Actions
- [ ] Test SqlDatabaseGiftList
- [ ] Automated tests for REST API
- [x] shields.io support for README badges
- [ ] Add linting to CI
- [x] Build and deploy docker image(s) to dockerhub via CI/CD
- [x] Deploy flask app to Heroku for [demo](https://online-store-flask-rest-api.herokuapp.com/) purposes (follow link)

## Future Improvements 🔮

Given more time, the following improvements could be made:

- [ ] Write frontend in React (or maybe Vue.js)
- [ ] Create `docker-compose.yml` multi-container Docker compose script for orchestrating frontend, backend and database (e.g. React/NPM-based, Flask, Postgres).
- [ ] Implement missing features in the code (i.e. wherever `NotImplementError` is raised)
- [ ] Code tidy and refactor
- [ ] Increase overall code coverage (aiming for nirvana at 100%)
