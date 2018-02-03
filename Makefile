SETTINGS=runblueprint.local_settings

.DEFAULT_GOAL: all
.PHONY: test

all: migrate test runserver

migrate:
	@echo "\n⭐  Running migrations...\n"
	venv/bin/python runblueprint/manage.py migrate --settings=$(SETTINGS);

test:
	@echo "\n⭐  Running tests...\n"
	venv/bin/python runblueprint/manage.py test -v 2 --settings=$(SETTINGS);

runserver:
	@echo "\n⭐  Running development server...\n"
	venv/bin/python runblueprint/manage.py runserver --settings=$(SETTINGS);

deploy:
	@echo "\n⭐  Deploying to Test...\n"
	@echo "❗  TBD..."


production:
	@echo "\n⭐  Deploying to Production...\n"
	@echo "❗  TBD..."
