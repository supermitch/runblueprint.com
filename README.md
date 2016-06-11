# runblueprint.com

Running training plan generator.

# Installation

You should only need to do these steps once:

* Download [Python 3.5+](https://www.python.org/downloads/)
* Clone repo
* Make virtual env in repo root: `$ python3 -m venv venv`
* Activate venv: `$ source venv/bin/activate`
* Upgrade pip: `$ pip install -U pip`
* Setup database (see below)

## Database Setup

* Install Postgresql 9.3+
* Create user and database

```bash
$ psql
> CREATE USER <username> WITH ENCRYTED PASSWORD <password>;
> CREATE DATABASE <dbname> WITH OWNER <username>;
> GRANT ALL PRIVILEGES ON DATABASE <dbname> TO <username>;
```

# Dev

Every time you work you need to do these steps:

* Activate venv: `$ source venv/bin/activate`
* Install dependencies: `$ pip install -r requirements.txt`
* Run database migrations: `$ ./manage.py migrate --settings=runblueprint.local_settings`
* Run local server: `$ ./manage.py runserver --settings=runblueprint.local_settings`

Don't forget to freeze requirements if you installed new dependencies:

* `$ pip freeze > requirements.txt`

