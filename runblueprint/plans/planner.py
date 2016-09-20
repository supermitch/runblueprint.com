import collections
import datetime
import math
import uuid

from dateutil.relativedelta import *
from dateutil.rrule import *



class Plan():
    def __init__(self, weeks):
        self.id = uuid.uuid1().hex
        self.weeks = weeks  # List of weeks

    def __str__(self):
        return 'Plan {}: {} weeks'.format(self.id, len(self.weeks))

    @property
    def distance(self):
        return sum(x.distance for x in self.weeks)

    @property
    def time(self):
        return sum(x.time for x in self.weeks)

    def get_week(self, title):
        """ Find a week by title. """
        for week in self.weeks:
            if week.title.lower() == title:
                return week


class Week():
    _WeekTypes = collections.namedtuple('WeekTypes', 'Base Growth Work Peak Taper Race')
    Types = _WeekTypes(*_WeekTypes._fields)  # Define constants for Week Types

    def __init__(self, number, days):
        self.number = number
        self.days = days  # List of days
        self.title = ''
        self.type = ''
        self._plan_distance = 0  # Internal: planned distance for that week

    @property
    def distance(self):
        return sum(x.distance for x in self.days)

    @property
    def time(self):
        return sum(x.time for x in self.days)

    def __str__(self):
        return 'Week {}: "{}" ({}, {} km)'.format(self.number, self.title, self.type, self.distance)


class Day():
    def __init__(self, number, date):
        self.number = number
        self.date = date
        self.distance = 0
        self.time = 0
        self.type = None  # Run type, e.g. Easy, Tempo

    def __str__(self):
        return '{}. {} {}: {}'.format(self.number,
            self.date.strftime('%Y-%m-%d'),
            self.date.strftime('%a'),
            self.distance)



def generate_plan(form_data):
    plan = generate_blank_plan(form_data)

    determine_peak_week(plan, form_data)  # Sets peak week
    assign_week_types(plan, form_data)
    assign_mileages(plan, form_data)

    return plan


def assign_week_types(plan, form_data):
    for week in plan.weeks:
        week.type = Week.Types.Base  # Temporarily ALL weeks are base weeks!


def assign_mileages(plan, form_data):
    starting_mileage = determine_starting_mileage(form_data)
    peak_mileage = determine_peak_mileage(form_data)
    plan.weeks[0]._plan_distance = starting_mileage
    plan.get_week('peak week')._plan_distance = starting_mileage


def determine_starting_mileage(form_data):
    """
    Starting mileage is equal to steady mileage.

    Depends on:
    * steady_mileage
    """
    starting_mileage = form_data.steady_mileage
    return starting_mileage


def determine_peak_mileage(form_data):
    """
    Peak mileage is the max of 100 miles or the race_distance, whichever
    is smaller.

    Depends on:
    * race_distance
    """
    peak_mileage = max(160, form_data.race_distance)
    return peak_mileage


def generate_blank_plan(form_data):
    """
    A blank plan has all the days of training in it, including
    recovery block. But the no distances or workouts.
    """
    start_date = determine_plan_start(form_data.plan_start, form_data.week_day_start)
    end_date = add_recovery_block(form_data.race_date, form_data.recovery_weeks)
    all_dates = generate_plan_dates(start_date, end_date)
    all_days = list(Day(i, d) for i, d in enumerate(all_dates, start=1))
    all_weeks = list(Week(i, w) for i, w in enumerate(chunk_into_weeks(all_days), start=1))
    return Plan(all_weeks)


def determine_plan_start(plan_start, week_day_start):
    """
    Calculate when the plan's first day is, given that week 1 must start on
    the specified week_day_start.
    """
    delta_days = (7 - int(week_day_start) - plan_start.isoweekday()) % 7
    start_day = plan_start - datetime.timedelta(delta_days)
    return start_day


def determine_peak_week(plan, form_data):
    peak_day = form_data.race_date + relativedelta(weeks=-form_data.taper_length)
    for week in plan.weeks:
        for day in week.days:
            if day.date == peak_day:
                week.title = 'peak week'
                return week.number


def add_recovery_block(race_date, recovery_weeks):
    return race_date + relativedelta(weeks=+recovery_weeks)


def generate_plan_dates(start, end):
    return list(d.date() for d in rrule(DAILY, dtstart=start, until=end))


def chunk_into_weeks(seq, size=7):
    """ Chunks days into week batches. """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
