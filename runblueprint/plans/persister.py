import os.path

from django.core.files import File
from django.conf import settings

from . import renderer


def persist(plan):
    # TODO: does this work for PDF? probably not
    for format in renderer.FORMATS:
        filepath = os.path.join(settings.MEDIA_ROOT, plan.id + '.' + format)
        with open(filepath, 'w') as f:
            myfile = File(f)
            myfile.write(renderer.render(plan, format))

