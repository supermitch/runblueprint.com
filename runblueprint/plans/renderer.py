import logging

from django.template.loader import render_to_string


class Renderer():
    def __init__(self, plan):
        self.plan = plan  # raw plan object

    def render(self, mode='html'):
        renderers = {
            'html': self._html,
            'pdf': self._pdf,
            'text': self._text,
            'pickle': self._pickle,
        }
        return renderers[mode]()

    def _html(self):
        logging.info('Rendering html')
        return render_to_string('plans/render_plan.html', {'plan': self.plan})

    def _pdf(self):
        logging.info('Rendering pdf')
        pass

    def _text(self):
        logging.info('Rendering text')
        output = str(self.plan)
        for week in self.plan.weeks:
            output += '\n  ' + str(week)
            for day in week.days:
                output += '\n    ' + str(day)
        return output

    def _pickle(self):
        logging.info('Rendering pickle')
        pass
