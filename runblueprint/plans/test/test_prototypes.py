from django.test import TestCase

from plans.prototypes import weeks


class TestPrototypes(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_percentage_sums(self):
        for name, week in weeks.prototypes.items():
            result = sum(proto['percent_of_weekly_distance'] for proto in week.values())
            self.assertAlmostEqual(result, 1, places=3, msg='while testing <{}> week'.format(name))

    def test_number_of_days(self):
        for name, week in weeks.prototypes.items():
            self.assertEqual(len(week.keys()), 7, msg='while testing <{}> week'.format(name))
