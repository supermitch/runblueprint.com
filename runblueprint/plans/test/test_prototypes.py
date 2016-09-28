from django.test import TestCase

from plans.prototypes import weeks

class PrototypesTestCase(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_percentage_sums(self):
        """ Check weekly prototype mileage adds up to 100 %. """
        for name, week in weeks.prototypes.items():
            result = sum(proto['percent_of_weekly_distance'] for proto in week.values())
            self.assertAlmostEqual(result, 1, places=1, msg='while testing <{}> week'.format(name))

    def test_number_of_days(self):
        """ Make sure all weeks have 7 days. """
        for name, week in weeks.prototypes.items():
            self.assertEqual(len(week.keys()), 7, msg='while testing <{}> week'.format(name))
