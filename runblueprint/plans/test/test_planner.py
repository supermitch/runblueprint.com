import datetime

from django.test import TestCase

from plans.planner import *


class TestPlannerFunctions(TestCase):
    def setUp(self):
        class FormData():
            def __init__(self):
                self.plan_start = datetime.date('2016', '10', '11')  # Tuesday
                self.week_day_start = '0'  # Monday
        self.form_data = FormData()

    def test_determine_plan_start(self):
        start_date = determine_plan_start(self.form_data.plan_start, self.form_data.week_day_start)
        self.assertEqual(start_date, '2016-10-10')
