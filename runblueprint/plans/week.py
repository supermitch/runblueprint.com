from enum import Enum


Week_types = Enum('WeekTypes', 'Base Growth Work Taper Race Recovery')
Week_variants = Enum('WeekVariants', 'Rest')


class Week():
    def __init__(self, number, days):
        self.number = number
        self.days = days  # List of days
        self.title = ''
        self.type = None
        self.variant = None
        self.phase = None  # Mesocycle
        self._target_distance = 0  # Internal: planned distance for that week

    @property
    def distance(self):
        return sum(day.distance for day in self.days)

    @property
    def time(self):
        return sum(day.time for day in self.days)

    def shortest_day(self):
        return sorted(self.days, key=lambda d:d.distance)[0]

    def __str__(self):
        return 'Week {}: {} - {:.1f} km'.format(self.number, self.title, self.distance)
