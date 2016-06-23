import math
import uuid

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

    weeks_count = determine_plan_length(form_data)  # TODO: Pass args
    for _ in range(weeks_count):
        plan.weeks.append(plan_week())
    return plan


def determine_plan_length(form_data):
    plan_start = form_data['plan_start']
    race_date = form_data['race_date']  # TODO: args
    datediff = relativedelta(plan_start, race_date)
    print('Start: {}, End: {}, diff: {}'.format(plan_start, race_date, datediff))
    return math.ceil(datediff.weeks)

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
