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
  * Note: User needs permission to create test DB (line 4)

```bash
$ psql
> CREATE USER <username> WITH ENCRYPTED PASSWORD <password>;
> CREATE DATABASE <dbname> WITH OWNER <username>;
> GRANT ALL PRIVILEGES ON DATABASE <dbname> TO <username>;
> ALTER USER <username> CREATEDB;
```

# Development

Every time you work you need to do these steps:

* Activate venv: `$ source venv/bin/activate`
* Install dependencies: `$ pip install -r requirements.txt`
* Run database migrations: `$ ./manage.py migrate --settings=runblueprint.local_settings`
  * Note that you need a `local_settings.py` file with your DB settings, at least!
* Run local server: `$ ./manage.py runserver --settings=runblueprint.local_settings`
  * (Or `make runserver`)

Don't forget to freeze requirements if you installed new dependencies:

* `$ pip freeze > requirements.txt`

## Production

RBP is running on AWS Elastic Beanstalk. Use the EB CLI client to interact
with the app and environment.

* [Command Reference](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-cmd-commands.html)

**Currently there is no test environment!**

## Makefile

Some handy shortcuts in the Makefile

* Start development server: `$ make runserver`
* Run tests: `$ make test`
* Deploy to **Production**: `$ make deploy`


