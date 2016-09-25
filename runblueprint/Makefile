.PHONY: test

test:
	. venv/bin/activate; \
	./manage.py test --settings=runblueprint.local_settings;

runserver:
	. venv/bin/activate; \
	./manage.py runserver --settings=runblueprint.local_settings;

deploy:
	. venv/bin/activate; \
	eb deploy;
