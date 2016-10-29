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

    # Column width for Day Type
    day_type_width = max(len(day.type.name) for week in plan.weeks for day in week.days)

    for week in plan.weeks:
        output += '\n\n  ' + str(week)
        for day in week.days:
            output += '\n {:>4}. {}  {}  {:<{fill}}'.format(day.number,
                    day.date.strftime('%Y-%m-%d'), day.date.strftime('%a'),
                    day.type.name, fill=day_type_width)
            if day.distance > 0:
                output += ' {:>5.1f}'.format(day.distance)
            output += '  ' + day.workout
    return output

