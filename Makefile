SETTINGS=runblueprint.local_settings

.DEFAULT_GOAL: all
.PHONY: test

all: migrate test runserver

migrate:
	@echo "\n⭐  Running migrations\n"
	venv/bin/python runblueprint/manage.py migrate --settings=$(SETTINGS)

test:
	@echo "\n⭐  Running tests\n"
	venv/bin/python runblueprint/manage.py test -v 2 --settings=$(SETTINGS)

runserver:
	@echo "\n⭐  Running development server\n"
	venv/bin/python runblueprint/manage.py runserver --settings=$(SETTINGS)

staging:
	@echo "\n⭐  Deploying to Staging\n"
	venv/bin/ansible-playbook -i ansible/hosts/staging ansible/django.yml --extra-vars "proceed=y"

production:
	@echo "\n❗❗ Deploying to Production\n"
	venv/bin/ansible-playbook -i ansible/hosts/production ansible/django.yml
