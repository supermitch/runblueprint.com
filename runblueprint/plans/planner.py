import collections
import datetime
import logging
import math
import uuid

from dateutil.relativedelta import *
from dateutil.rrule import *

from .prototypes import weeks



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

    def get(self, title):
        """ Find a week by title, return (index, week) tuple. """
        for i, week in enumerate(self.weeks):
            if week.title.lower() == title:
                return i, week

class Week():
    WeekTypes = ('Base', 'Growth', 'Work', 'Peak', 'Taper', 'Race', 'Recovery')
    Types = collections.namedtuple('WeekTypes', WeekTypes)(*WeekTypes)  # Define constants for Week Types

    def __init__(self, number, days):
        self.number = number
        self.days = days  # List of days
        self.title = ''
        self.type = ''
        self._target_distance = 0  # Internal: planned distance for that week

    @property
    def distance(self):
        return sum(x.distance for x in self.days)

    @property
    def time(self):
        return sum(x.time for x in self.days)

    def __str__(self):
        return 'Week {}: "{}" ({}, {} km)'.format(self.number, self.title, self.type, math.ceil(self.distance))

class Day():
    def __init__(self, number, date):
        self.number = number
        self.date = date
        self.distance = 0
        self.time = 0
        self.type = ''  # Run type, e.g. Easy, Tempo

    def __str__(self):
        return '{}. {} {}: {} {}'.format(self.number, self.date.strftime('%Y-%m-%d'),
            self.date.strftime('%a'), self.type, math.ceil(self.distance))



def generate_plan(form_data):
    plan = generate_blank_plan(form_data)

    assign_week_types(plan, form_data)
    assign_weekly_distance(plan, form_data)
    apply_week_prototypes(plan)

    return plan


def assign_week_types(plan, form_data):
    # Set Base weeks
    for week in plan.weeks:
        week.type = Week.Types.Base  # Initially ALL weeks are base weeks!

    # Determine Peak Week
    peak_day = form_data.race_date + relativedelta(weeks=-form_data.taper_length)
    for i, week in enumerate(plan.weeks):
        for day in week.days:
            if day.date == peak_day:
                week.title = 'peak week'
                peak_index = i

    for week in plan.weeks[peak_index + 1:peak_index + form_data.taper_length + 1]:
        week.type = Week.Types.Taper

    # Set Recovery weeks
    for week in plan.weeks[-form_data.recovery_weeks:]:
        week.type = Week.Types.Recovery


def assign_weekly_distance(plan, form_data):
    """ Assign weekly mileage targets to each of our plan's weeks. """
    start_dist = determine_starting_mileage(form_data)  # TODO: Week 0 might be a base phase and not actually use the "starting mileage" value
    peak_dist = determine_peak_mileage(form_data)

    start_idx = 0
    peak_idx, _ = plan.get('peak week')

    for i, week in enumerate(plan.weeks[:peak_idx + 1]):  # Fill in from weeks 0 to peak week
        target_distance = start_dist + (peak_dist - start_dist) / (peak_idx - start_idx) * i  # Linearly increase in mileage from start to peak
        week._target_distance = target_distance


def apply_week_prototypes(plan):
    """ Apply the weekly prototype data to the individual days, e.g. distance, type. """
    for week in plan.weeks:
        week_proto = weeks.prototypes[week.type]
        for day in week.days:
            day_of_the_week = day.number % 7
            day_proto = week_proto[day_of_the_week]
            day.distance = week._target_distance * day_proto['percent_of_weekly_distance']
            day.type = day_proto['type']


def determine_starting_mileage(form_data):
    """
    Starting mileage is equal to steady mileage.

    Depends on: steady_mileage
    """
    return form_data.steady_mileage if form_data.steady_mileage is not None else 40


def determine_peak_mileage(form_data):
    """
    Peak mileage is the max of 100 miles or the race_distance, whichever is smaller.

    Depends on: race_distance
    """
    return max(160, form_data.race_distance)


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


def add_recovery_block(race_date, recovery_weeks):
    return race_date + relativedelta(weeks=+recovery_weeks)


def generate_plan_dates(start, end):
    return list(d.date() for d in rrule(DAILY, dtstart=start, until=end))


def chunk_into_weeks(seq, size=7):
    """ Chunks days into week batches. """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
