# Runblueprint.com

Running training plan generator.

See Trello project at https://trello.com/b/X6Fg9XVA/runblueprint

# Requirements

* Install [Pyenv](https://github.com/pyenv/pyenv#basic-github-checkout)
* `brew install mysql` (5.7.x)

# Installation

You should only need to do these steps once:

```bash
pyenv install 3.6.3
pyenv global 3.6.3
git clone git@github.com:supermitch/runblueprint.com.git
cd runblueprint
python -m venv venv
source venv/bin/activate
pip install -U pip
```

## Database Setup

Note that you need a `local_settings.py` file with your DB settings, at least!

* Create user & database
  * Note: User needs permission to create test DB (line 4)

```bash
$ mysql
> CREATE USER <username> WITH ENCRYPTED PASSWORD <password>;
> CREATE DATABASE <dbname> WITH OWNER <username>;
> GRANT ALL PRIVILEGES ON DATABASE <dbname> TO <username>;
> ALTER USER <username> CREATEDB;
```

# Development

Every time you work you should do these steps:

```bash
source venv/bin/activate
pip install -r requirements.txt
make migrate
```

Don't forget to freeze requirements if you installed new dependencies:

```bash
pip freeze > requirements.txt
```

## Production

No production environment yet... TBD.

## Makefile

Some handy shortcuts in the Makefile

* `$ make` - Start local development server: http://127.0.0.1:8000
* `$ make test` - Run tests
* `$ make migrate` - Run migrations
* `$ make deploy` - Deploy to **Test** *TBD*
* `$ make production` - Deploy to **Production** *TBD*

## Create Superuser

Instructions to create a user that can login to the admin site.

* `$ source venv/bin/activate` - Make sure you are in the virtual env
* `$ ./manage.py createsuperuser --settings=runblueprint.local_settings` - Run createsuperuser command
* Follow user creation prompts
* Test new superuser login at http://127.0.0.1:8000/admin/
