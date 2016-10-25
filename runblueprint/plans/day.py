from enum import Enum


Day_types = Enum('DayTypes', ['Recovery', 'Easy', 'Long', 'Quality', 'Rest', 'Crosstrain'])


class Day():
    def __init__(self, number, date):
        self.number = number
        self.date = date
        self.distance = 0
        self.time = 0
        self.type = ''  # Run type, e.g. Easy, Tempo
        self.workout = ''  # Workout details, e.g. '2 mi E + 4 x (2 min T ...'

    def __str__(self):
        return '{}. {} {}: {} {:.1f}'.format(self.number, self.date.strftime('%Y-%m-%d'),
            self.date.strftime('%a'), self.type, self.distance)



