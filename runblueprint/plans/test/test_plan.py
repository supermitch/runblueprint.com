from django.test import TestCase

from plans.plan import Plan
from plans.week import Week, Week_types


class TestPlanMethods(TestCase):
    def setUp(self):
        weeks = []
        for i in range(5):
            week = Week(i, [])  # Empty week
            if i < 2:
                week.type = Week_types.Taper
            else:
                week.type = Week_types.Recovery
            weeks.append(week)
        self.plan = Plan('Test Race', weeks)

    def test_count_weeks_by_type(self):
        result = self.plan.count_weeks_by_type(Week_types.Taper)
        self.assertEqual(result, 2)
