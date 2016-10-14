from django.test import TestCase

from plans.planner import Plan, Week


class TestPlanMethods(TestCase):
    def setUp(self):
        weeks = []
        for i in range(5):
            week = Week(i, [])  # Empty week
            if i < 2:
                week.type = Week.Types.Taper
            else:
                week.type = Week.Types.Recovery
            weeks.append(week)
        self.plan = Plan('Test Race', weeks)

    def test_count_weeks_by_type(self):
        result = self.plan.count_weeks_by_type(Week.Types.Taper)
        self.assertEqual(result, 2)

        result = self.plan.count_weeks_by_type('Recovery')  # Works with strings
        self.assertEqual(result, 3)
