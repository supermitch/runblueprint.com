import datetime
import math
import uuid

from dateutil.relativedelta import *
from dateutil.rrule import *


class Plan():
    def __init__(self, weeks):
        self.id = uuid.uuid1().hex
        self.weeks = weeks

    def __str__(self):
        return 'Plan {}: {} weeks'.format(self.id, len(self.weeks))

    @property
    def distance(self):
        return sum(x.distance for x in self.weeks)

    @property
    def time(self):
        return sum(x.time for x in self.weeks)


class Week():
    def __init__(self, number, days):
        self.number = number
        self.days = days

    @property
    def distance(self):
        return sum(x.distance for x in self.days)

    @property
    def time(self):
        return sum(x.time for x in self.days)


class Day():
    def __init__(self, number, date):
        self.number = number
        self.date = date


def sanity_check(data):
    return "{}, your plan is {} weeks long.".format(data['your_name'], data['weeks'])


def generate_plan(form_data):

    start_date = determine_plan_start(form_data['plan_start'], form_data['week_day_start'])
    end_date = form_data['end_date']  # TODO: Get end date after recovery block

    all_dates = generate_plan_dates(start_date, end_date)

    all_days = list(Day(i, d) for i, d in enumerate(all_dates, start=1))

    all_weeks = list(Week(i, w) for i, w in enumerate(chunk_into_weeks(all_days), start=1))

    plan = Plan(all_weeks)

    return plan


def determine_plan_start(plan_start, week_day_start):
    """
    Calculate when the plan's first day is, given that week 1 must start on
    the specified week_day_start.
    """
    delta_days = (7 - int(week_day_start) - plan_start.isoweekday()) % 7
    start_day = plan_start - datetime.timedelta(delta_days)
    return start_day


def generate_plan_dates(start, end):
    return list(rrule(DAILY, dtstart=start, until=end))


def chunk_into_weeks(seq, size=7):
    """ Chunks days into week batches. """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def determine_plan_length(form_data):
    pass


def plan_week():
    week = {'days': [],
            'total_dist': 0}
    days = 7
    for i in range(0, 7):
        week['days'].append({'day': i, 'dist': 5})
    return week

def stringify_plan(plan):
    """print plan out to console for debugging"""
    print(plan)
