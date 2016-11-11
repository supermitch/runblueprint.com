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


    def test_needs_race_week_recovery(self):
        race_date = datetime.date(2016, 11, 8)  # Tue
        start_date = datetime.date(2016, 11, 7)  # Mon
        self.assertEqual(needs_race_week(race_date, start_date), False)

    def test_needs_race_week_true(self):
        race_date = datetime.date(2016, 11, 10)  # Thu
        start_date = datetime.date(2016, 11, 7)  # Mon
        self.assertEqual(needs_race_week(race_date, start_date), True)

    def test_needs_race_week_taper(self):
        race_date = datetime.date(2016, 11, 14)  # Sat
        start_date = datetime.date(2016, 11, 7)  # Mon
        self.assertEqual(needs_race_week(race_date, start_date), False)


    def test_determine_recovery_start_taper(self):
        start_date = datetime.date(2016, 11, 7)  # Mon
        race_date = datetime.date(2016, 11, 8)  # Tue # Should start on Monday before the race
        self.assertEqual(determine_recovery_start(race_date, start_date), datetime.date(2016, 11, 6))

    def test_determine_recovery_start_recovery(self):
        start_date = datetime.date(2016, 11, 7)  # Mon
        race_date = datetime.date(2016, 11, 9)  # Wed # Should start on first Monday after race
        self.assertEqual(determine_recovery_start(race_date, start_date), datetime.date(2016, 11, 13))

    def test_determine_recovery_start_race_week(self):
        start_date = datetime.date(2016, 11, 7)  # Mon
        race_date = datetime.date(2016, 11, 12)  # Sat # Should start on Monday after the race
        self.assertEqual(determine_recovery_start(race_date, start_date), datetime.date(2016, 11, 13))
