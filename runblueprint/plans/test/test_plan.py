import datetime

from django.test import TestCase

from plans.plan import Plan
from plans.week import Week, Week_types
from plans.day import Day


class TestPlanMethods(TestCase):
    def setUp(self):
        self.days = []  # Build a set of days
        for i in range(35):
            day = Day(i, datetime.date(2016, 1, 1))  # Normally not all the same date!
            if i < 28:
                day.distance = i * 10  # Add some distance to each
            else:
                day.distance = 5  # Last week is a rest
            self.days.append(day)

        self.weeks = []  # Build a set of weeks
        for i in range(5):
            week = Week(i, self.days[i * 7:(i + 1) * 7])  # Each week has 7 days
            if i < 2:
                week.type = Week_types.Taper
                week.title = 'Base week'
            else:
                week.type = Week_types.Recovery
            self.weeks.append(week)

        self.plan = Plan('Test Race', self.weeks)

    def test_peak_week(self):
        self.assertEqual(self.plan.peak_week(), self.weeks[3])

    def test_get_by_title(self):
        result = self.plan.get_by_title('Base week')
        self.assertEqual(result, (0, self.weeks[0]))

    def test_get_by_title_part(self):
        self.plan.weeks[0].title = 'Endurance week / Base week'  # Multiple titles
        result = self.plan.get_by_title('Base week')
        self.assertEqual(result, (0, self.weeks[0]))

    def test_count_weeks_by_type(self):
        result = self.plan.count_weeks_by_type(Week_types.Taper)
        self.assertEqual(result, 2)

    def test_get_week_by_type(self):
        result = self.plan.get_weeks_by_type(Week_types.Recovery)
        self.assertEqual(result, [(2, self.weeks[2]), (3, self.weeks[3]), (4, self.weeks[4])])
