import os
import sys


cwd = os.getcwd()

INTERP = os.path.join(cwd, 'venv/bin/python')
# INTERP is present twice so that the new python interpreter knows the actual executable path:
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.append(cwd)
sys.path.append(cwd + '/runblueprint/')  # You must add your project here

sys.path.insert(0, cwd + 'venv/bin')
sys.path.insert(0, cwd + 'venv/lib/python3.6/site-packages/django')
sys.path.insert(0, cwd + 'venv/lib/python3.6/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'runblueprint.local_settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
