import math
import uuid

import datetime
from dateutil.relativedelta import *


class Plan():
    def __init__(self):
        self.id = uuid.uuid1().hex
        self.weeks = []

    def __str__(self):
        return 'Plan {}: {} weeks'.format(self.id, len(self.weeks))


def sanity_check(data):
    return "{}, your plan is {} weeks long.".format(data['your_name'], data['weeks'])


def generate_plan(form_data):
    plan = Plan()

    start_date = determine_plan_start(form_data['plan_start'], form_data['week_day_start'])
    weeks_count = 26
    for _ in range(weeks_count):
        plan.weeks.append(plan_week())
    return plan


def determine_plan_start(plan_start, week_day_start):
    idx = plan_start.isoweekday() % 7  # MON = 0, SUN = 6 -> SUN = 0 .. SAT = 6
    print(idx)
    print(week_day_start)
    start_day = plan_start - datetime.timedelta(7 + idx - int(week_day_start))
    print(start_day.isoweekday())
    return start_day


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
