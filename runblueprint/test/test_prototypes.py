import logging

from django.test import TestCase

from plans.prototypes import weeks


class PrototypesTestCase(TestCase):
    def setup(self):
        pass

    def test_percentage_sums(self):
        """ Check weekly prototype mileage adds up to 100 %. """
        for name, week in weeks.prototypes.items():
            logging.info('Testing week <{}>'.format(name))
            result = sum(proto['percent_of_weekly_distance'] for proto in week.values())
            self.assertAlmostEqual(result, 1, places=1)
