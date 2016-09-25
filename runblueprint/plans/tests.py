from django.test import TestCase
from plans.planner import Plan

data = {'weeks': 4,
        'race_dist': 10,
        'race_terrain': None,
        'goal_time': 0}

class PlanTestCase(TestCase):
    def setup(self):
        pass

    def test_plan_is_correct_length(self):
        """ Plan should use all days between now and race. """
        my_plan = Plan(data)
        print(my_plan)
        self.assertEqual(len(my_plan), 4)

