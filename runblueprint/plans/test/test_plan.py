from django.test import TestCase

from plans.plan import Plan
from plans.week import Week, Week_types


class TestPlanMethods(TestCase):
    def setUp(self):
        self.weeks = []
        for i in range(5):
            week = Week(i, [])  # Empty week
            if i < 2:
                week.type = Week_types.Taper
            else:
                week.type = Week_types.Recovery

            if i < 3:
                week.title = 'Base'

            self.weeks.append(week)
        self.plan = Plan('Test Race', self.weeks)

    def test_get_by_title(self):
        result = self.plan.get_by_title('Base')
        self.assertEqual(result, (0, self.weeks[0]))

    def test_count_weeks_by_type(self):
        result = self.plan.count_weeks_by_type(Week_types.Taper)
        self.assertEqual(result, 2)

    def test_get_week_by_type(self):
        result = self.plan.get_weeks_by_type(Week_types.Recovery)
        self.assertEqual(result, [(2, self.weeks[2]), (3, self.weeks[3]), (4, self.weeks[4])])
