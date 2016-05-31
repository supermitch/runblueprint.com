from django.test import TestCase
from .planner import plan

data = {'weeks': 4,
        'race_dist': 10,
        'race_terrain': None,
        'goal_time': 0}

class PlanTestCase(TestCase):
    def setup(self):
        pass

    def test_plan_is_correct_length(self):
        """plan should use all days between now and race"""
        my_plan = plan(data)
        print(my_plan)
        self.assertEqual(len(my_plan), 4)

