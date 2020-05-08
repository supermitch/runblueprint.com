import datetime

from django.test import SimpleTestCase

from plans.planner import *


class TestPlannerFunctions(SimpleTestCase):
    def setUp(self):
        pass

    def assert_listAlmostEqual(self, list1, list2):
        self.assertEqual(len(list1), len(list2))

        for (fst, snd) in zip(list1, list2):
            self.assertAlmostEquals(fst, snd)

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
        race_date = datetime.date(2016, 11, 8)  # Tue
        start_date = datetime.date(2016, 11, 7)  # Mon
        result = determine_recovery_start(race_date, start_date)
        self.assertEqual(result, datetime.date(2016, 11, 6))  # Should start on Monday before the race

    def test_determine_recovery_start_recovery(self):
        race_date = datetime.date(2016, 11, 9)  # Wed
        start_date = datetime.date(2016, 11, 7)  # Mon
        result = determine_recovery_start(race_date, start_date)
        self.assertEqual(result, datetime.date(2016, 11, 13))  # Should start on first Monday after race

    def test_determine_recovery_start_race_week(self):
        race_date = datetime.date(2016, 11, 12)  # Sat
        start_date = datetime.date(2016, 11, 7)  # Mon
        result = determine_recovery_start(race_date, start_date)
        self.assertEqual(result, datetime.date(2016, 11, 13))  # Should start on Monday after the race

    def test_get_recovery_percent_4(self):
        total_weeks = 4

        recovery_percents = get_weekly_recovery_percents(total_weeks)

        self.assert_listAlmostEqual([0.2, 0.4, 0.6, 0.8], recovery_percents)

    def test_get_recovery_percent_4(self):
        total_weeks = 3

        recovery_percents = get_weekly_recovery_percents(total_weeks)

        self.assert_listAlmostEqual([0.25, 0.5, 0.75], recovery_percents)

    def test_get_recovery_percent_1(self):
        total_weeks = 1

        recovery_percents = get_weekly_recovery_percents(total_weeks)

        self.assert_listAlmostEqual([0.5], recovery_percents)

    def test_get_recovery_percent_0(self):
        total_weeks = 0

        recovery_percents = get_weekly_recovery_percents(total_weeks)

        self.assert_listAlmostEqual([], recovery_percents)

    def test_get_recovery_percent_negative(self):
        total_weeks = -1

        recovery_percents = get_weekly_recovery_percents(total_weeks)

        self.assert_listAlmostEqual([], recovery_percents)

    def test_get_recovery_dists_1(self):
        total_weeks = 1
        post_recovery_dist = 20.0
        recovery_dists = get_weekly_recovery_dists(total_weeks, post_recovery_dist)

        self.assert_listAlmostEqual([post_recovery_dist/2.0], recovery_dists)

    def test_get_recovery_dists_2(self):
        total_weeks = 2
        post_recovery_dist = 20.0
        recovery_dists = get_weekly_recovery_dists(total_weeks, post_recovery_dist)

        self.assert_listAlmostEqual([post_recovery_dist/3.0, post_recovery_dist * (2.0/3.0)], recovery_dists)

    def test_get_recovery_dists_negative_weeks(self):
        total_weeks = -1
        post_recovery_dist = 20.0

        recovery_dists = get_weekly_recovery_dists(total_weeks, post_recovery_dist)

        self.assert_listAlmostEqual([], recovery_dists)

    def test_get_recovery_dists_negative_dist(self):
        total_weeks = 1
        post_recovery_dist = -15.0

        self.assertRaises(ValueError, get_weekly_recovery_dists, total_weeks, post_recovery_dist)

    def test_assign_recovery_dists_single_week(self):
        days = [Day(0, datetime.date(2016, 1, 1))]
        weeks = [Week(1, days)]

        post_recovery_dist = 15.0
        assign_recovery_week_dists(weeks, post_recovery_dist)
        self.assertAlmostEqual(weeks[0]._target_distance, post_recovery_dist/2.0)

    def test_are_indices_continuous_empty(self):
        indices = []
        self.assertTrue(are_indices_continuous(indices))

    def test_are_indices_continuous_single(self):
        indices = [1]
        self.assertTrue(are_indices_continuous(indices))

    def test_are_indices_continuous_double(self):
        indices = [1, 2]
        self.assertTrue(are_indices_continuous(indices))

    def test_are_indices_continuous_separated(self):
        indices = [1, 3]
        self.assertFalse(are_indices_continuous(indices))

    def test_are_indices_continuous_triple(self):
        indices = [1, 2, 3]
        self.assertTrue(are_indices_continuous(indices))

