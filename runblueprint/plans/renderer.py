import logging

from django.template.loader import render_to_string

from plans.day import Day_types


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
    output = str(plan)  # Add Plan description

    day_type_width = max(len(day.type.name) for week in plan.weeks for day in week.days)  # Column width for Day Type

    current_phase = None
    for week in plan.weeks:

        if not current_phase or week.phase != current_phase:
            # TODO: Get Phase name width and fill
            output += '\n\n\n ========== Phase {} - {} ==========\n'.format(week.phase.value, week.phase.name)
            current_phase = week.phase

        # TODO: Capitalize RACE in Week description
        output += '\n\n ' + str(week)  # Add Week description

        for day in week.days:
            if day.type == Day_types.Race:
                output += '\n --------------------------------------'
                day_name = day.type.name.upper() + '!'  # RACE!
            else:
                day_name = day.type.name

            output += '\n{:>4}. {}  {}  {:<{fill}}'.format(day.number,
                    day.date.strftime('%Y-%m-%d'), day.date.strftime('%a'),
                    day_name, fill=day_type_width)
            if day.distance > 0:
                output += ' {:>5.1f}'.format(day.distance)
            output += '  ' + day.workout

            if day.type == Day_types.Race:
                output += '\n --------------------------------------'

    return output
