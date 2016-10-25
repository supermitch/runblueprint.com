from enum import Enum


Week_types = Enum('WeekTypes', ['Base', 'Growth', 'Work', 'Taper', 'Race', 'Recovery'])
Week_variants = Enum('WeekVariants', ['Rest'])


class Week():
    def __init__(self, number, days):
        self.number = number
        self.days = days  # List of days
        self.title = ''
        self.type = ''
        self.variant = ''
        self.phase = None  # Mesocycle (int, 1-5)  # TODO: Use enum
        self._target_distance = 0  # Internal: planned distance for that week

    @property
    def distance(self):
        return sum(day.distance for day in self.days)

    @property
    def time(self):
        return sum(day.time for day in self.days)

    def __str__(self):
        return 'Week {}: {} - {:.1f} km - Phase {}'.format(self.number, self.title, self.distance, self.phase)

