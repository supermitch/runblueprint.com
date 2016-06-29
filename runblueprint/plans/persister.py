import os.path

from django.core.files import File
from django.conf import settings


def persist(plan):
    # TODO: does this work for PDF? probably not
    formats = [  # TODO: tight coupling is bad!
        ('text', '.txt'),
        ('html', '.html'),
        # ('pdf', '.pdf'),
    ]
    for format, extension in formats:
        filepath = os.path.join(settings.MEDIA_ROOT, plan.id + extension)
        with open(filepath, 'w') as f:
            myfile = File(f)
            myfile.write(plan.render_as(format))

