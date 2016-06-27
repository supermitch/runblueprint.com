import datetime
import math
import uuid

from dateutil.relativedelta import *
from dateutil.rrule import *

from . import renderer


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

    def render_as(self, mode):
        return renderer.Renderer(self).render(mode)


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

    def __str__(self):
        return 'Week {}: {}'.format(self.number, self.distance)


class Day():
    def __init__(self, number, date):
        self.number = number
        self.date = date
        self.distance = 0
        self.time = 0

    def __str__(self):
        return 'Day {}: {}'.format(self.number, self.distance)


def generate_plan(form_data):
    blank_plan = generate_blank_plan(form_data)
    # TODO: Actually fill in the plan
    plan = blank_plan
    return plan


def generate_blank_plan(form_data):

    start_date = determine_plan_start(form_data['plan_start'], form_data['week_day_start'])

    end_date = add_recovery_block(form_data['race_date'])

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


def add_recovery_block(race_date):
    # TODO: Variable length recovery block
    return race_date + relativedelta(weeks=+5)


def generate_plan_dates(start, end):
    return list(rrule(DAILY, dtstart=start, until=end))


def chunk_into_weeks(seq, size=7):
    """ Chunks days into week batches. """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
