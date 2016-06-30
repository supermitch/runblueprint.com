import os

from django.core.files import File
from django.conf import settings

from . import renderer

def persist(plan):
    media_root = settings.MEDIA_ROOT
    if not os.path.exists(media_root):
        os.makedirs(media_root)

    # TODO: does this work for PDF? probably not
    for format in renderer.FORMATS:
        filepath = os.path.join(media_root, plan.id + '.' + format)
        with open(filepath, 'w') as f:
            myfile = File(f)
            myfile.write(renderer.render(plan, format))

