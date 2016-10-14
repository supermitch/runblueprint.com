import datetime

from django.test import SimpleTestCase

from plans.planner import *


class TestPlannerFunctions(SimpleTestCase):
    def setUp(self):
        pass

    def test_determine_plan_start_before(self):
        plan_start = datetime.date(2016, 10, 11)  # Tuesday
        week_day_start = 3  # Thursday
        start_date = determine_plan_start(plan_start, week_day_start)
        self.assertEqual(start_date, datetime.date(2016, 10, 6))

    def test_determine_plan_start_after(self):
        plan_start = datetime.date(2016, 10, 11)  # Tuesday
        week_day_start = 0  # Monday
        start_date = determine_plan_start(plan_start, week_day_start)
        self.assertEqual(start_date, datetime.date(2016, 10, 10))

    def test_determine_plan_start_exact(self):
        plan_start = datetime.date(2016, 10, 10)  # Monday
        week_day_start = 0  # Monday
        start_date = determine_plan_start(plan_start, week_day_start)
        self.assertEqual(start_date, datetime.date(2016, 10, 10))
