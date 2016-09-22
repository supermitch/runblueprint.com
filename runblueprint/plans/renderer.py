import logging

from django.template.loader import render_to_string


FORMATS = ['html', 'pdf', 'txt']

def render(plan, format='html'):
    logging.info('Rendering ' + format)
    renderers = {
        'html': _html,
        'pdf': _pdf,
        'txt': _txt,
    }
    return renderers[format](plan)


def _html(plan):
    return render_to_string('plans/render_plan.html', {'plan': plan})


def _pdf(plan):
    return ''


def _txt(plan):
    output = str(plan)
    for week in plan.weeks:
        output += '\n\n  ' + str(week)
        for day in week.days:
            output += '\n    ' + str(day)
    return output

