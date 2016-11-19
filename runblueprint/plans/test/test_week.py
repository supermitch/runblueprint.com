import datetime

from django.test import TestCase

from plans.week import Week
from plans.day import Day


class TestWeek(TestCase):
    def setUp(self):
        self.days = []
        for i in range(7):
            day = Day(i, datetime.date(2016, 1, 1))
            day.distance = i
            self.days.append(day)
        self.week = Week(1, self.days)

    def test_distance(self):
        self.assertEqual(self.week.distance, 21)

    def test_shortest_day(self):
        self.assertEqual(self.week.shortest_day(), self.days[0])
        self.assertEqual(self.week.shortest_day().distance, 0)

        self.week.days[2].distance = -2  # New shortest
        self.assertEqual(self.week.shortest_day(), self.days[2])

    def test_shortest_days(self):
        self.assertEqual(self.week.shortest_days(2), [self.days[0], self.days[1]])

        self.week.days[2].distance = -2  # New shortest
        self.assertEqual(self.week.shortest_days(3), [self.days[2], self.days[0], self.days[1]])
