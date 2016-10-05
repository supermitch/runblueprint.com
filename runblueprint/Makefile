.PHONY: test

migrate:
	. venv/bin/activate; \
	./manage.py migrate --settings=runblueprint.local_settings;

test:
	. venv/bin/activate; \
	./manage.py test -v 2 --settings=runblueprint.local_settings;

runserver:
	. venv/bin/activate; \
	./manage.py runserver --settings=runblueprint.local_settings;

deploy:
	. venv/bin/activate; \
	eb deploy;
