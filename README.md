# Runblueprint.com

Running training plan generator.

See Trello project at https://trello.com/b/X6Fg9XVA/runblueprint

# Requirements

* `brew install mysql`
* Python 3.6.x at least: suggest using [Pyenv](https://github.com/pyenv/pyenv#basic-github-checkout)

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

Create local user & database:
```bash
mysql.server start
mysql
CREATE USER 'runblueprint'@'localhost' IDENTIFIED WITH sha256_password BY 'runblueprint';
CREATE DATABASE IF NOT EXISTS runblueprint;
GRANT ALL PRIVILEGES ON `%_runblueprint`.* TO 'runblueprint'@'localhost';  # Allows test_runblueprint creation
SHOW GRANTS FOR 'runblueprint'@'localhost';  # Check it worked
```

# Development

Note that you need a `local_settings.py` file with your DB settings, at least!

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
* `$ make staging` - Deploy to **Staging** *TBD*
* `$ make production` - Deploy to **Production** *TBD*

## Create Superuser

Instructions to create a user that can login to the admin site.

* `$ source venv/bin/activate` - Make sure you are in the virtual env
* `$ ./manage.py createsuperuser --settings=runblueprint.local_settings` - Run createsuperuser command
* Follow user creation prompts
* Test new superuser login at http://127.0.0.1:8000/admin/
