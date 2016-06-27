class Renderer():
    def __init__(self, plan):
        self.plan = plan  # raw plan object

    def render_as(self, output='html'):
        renderers = {
            'html': self._html,
            'pdf': self._pdf,
            'text': self._text,
            'pickle': self._pickle,
        }
        return renderers[output]()

    def _html(self):
        logging.info('Rendering html')
        return '<b>PLAN!</b>'

    def _pdf(self):
        logging.info('Rendering pdf')
        pass

    def _text(self):
        logging.info('Rendering text')
        return str(self.plan)

    def _pickle(self):
        logging.info('Rendering pickle')
        pass
