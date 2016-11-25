import collections
import datetime
import enum
import logging
import math
import random

from dateutil.relativedelta import *
from dateutil.rrule import *

from plans.week import Week, Week_types, Week_variants
from plans.plan import Plan, Phases
from plans.day import Day, Day_types
from plans.prototypes import weeks, workouts


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


def generate_plan(form_data):
    plan = generate_blank_plan(form_data)

    assign_phases(plan, form_data)
    assign_week_types(plan, form_data)
    assign_variants(plan, form_data)
    assign_weekly_distance(plan, form_data)
    apply_week_prototypes(plan, form_data)
    assign_quality(plan, form_data)
    assign_daily_distances(plan, form_data)
    assign_week_titles(plan, form_data)

    return plan


def assign_week_types(plan, form_data):
    race_week = 1 if needs_race_week(form_data.race_date, plan.start_date) else 0
    for i, week in enumerate(plan.weeks[::-1]):  # Work backwards
        if i < form_data.recovery_weeks:
            week.type = Week_types.Recovery
        elif race_week and i < form_data.recovery_weeks + race_week:
            week.type = Week_types.Race
        elif i < form_data.recovery_weeks + race_week + form_data.taper_length:
            week.type = Week_types.Taper
        elif i < form_data.recovery_weeks + race_week + form_data.taper_length + 18:
            week.type = Week_types.Work
        else:
            week.type = Week_types.Base


def assign_variants(plan, form_data):
    for i, week in enumerate(plan.weeks):
        if (i + 1) % 4 == 0:  # Every 4th week
            if week.type in (Week_types.Base, Week_types.Work):  # Other phases have no rest weeks
                week.variant = Week_variants.Rest


def assign_weekly_distance(plan, form_data):
    """ Assign weekly mileage targets to each of our plan's weeks. """
    start_dist = determine_starting_mileage(form_data)  # TODO: Week 0 might be a base phase and not actually use the "starting mileage" value
    peak_dist = determine_peak_mileage(form_data)
    delta_dist = peak_dist - start_dist
    print('start: {}, end: {}, delta: {}'.format(start_dist, peak_dist, delta_dist))

    start_index = 0  # TODO: Week 0 might be a base phase and not actually use the "starting mileage" value
    for i, week in enumerate(plan.weeks):
        if week.type == Week_types.Taper:
            taper_index = i  # First week before Taper is the peak week
            break
    weeks = taper_index - start_index - 4  # -4 b/c we do one month at base mileage
    months = math.ceil(weeks / 4)  # math.ceil so last month is at peak mileage even if only one week.

    # Set work volumes
    # TODO: set distances differently for base & work phases
    for i, week in enumerate(plan.weeks[:taper_index]):  # Fill in from weeks 0 to peak week, inclusive
        if form_data.growth_method == 'gradual':  # Weekly increases
            target_distance = start_dist + delta_dist * i / weeks  # Linearly increase in mileage from start to peak
        else:  # Daniels monthly increases
            month = math.floor(i / 4)  # Increase mileage every 4 weeks
            target_distance = start_dist + delta_dist * month / months

        if week.variant == Week_variants.Rest:
            target_distance *= 0.6  # Rest week is 60 %

        week._target_distance = target_distance

    # Set taper volumes
    taper_count = plan.count_weeks_by_type(Week_types.Taper)
    if taper_count == 4:
        taper_percents = {1: 0.60, 2: 0.80, 3: 0.60, 4: 0.25}
    elif taper_count == 3:
        taper_percents = {1: 0.75, 2: 0.50, 3: 0.25}
    elif taper_count == 2:
        taper_percents = {1: 0.20, 2: 0.20}
    elif taper_count == 1:
        taper_percents = {1: 0.10}
    else:
        raise ValueError('Invalid number of taper weeks ({}). Must be from 0 to 4 weeks'.format(taper_count))

    for idx, (i, week) in enumerate(plan.get_weeks_by_type(Week_types.Taper), start=1):
        taper_percent = taper_percents[idx]
        week._target_distance = taper_percent * peak_dist

    for idx, (i, week) in enumerate(plan.get_weeks_by_type(Week_types.Recovery), start=1):
        recovery_percent = {1: 0.20, 2: 0.36, 3: 0.43, 4: 0.50, 5: 0.59}[idx]
        week._target_distance = recovery_percent * peak_dist


def assign_week_titles(plan, form_data):
    """ Turn types into titles. """
    counter = 0
    last_type = None
    for i, week in enumerate(plan.weeks):
        try:
            if week.type == last_type:  # If this week type is the same as the last
                counter += 1
                week.title = '{} week {}'.format(week.type.name.capitalize(), counter)
            else:  # It's a new type, or the first week
                counter = 1
                if week.type == plan.weeks[i + 1].type:  # Only add a 1 if next week is a 2!
                    week.title = week.type.name.capitalize() + ' week 1'
                else:
                    week.title = week.type.name.capitalize() + ' week'  # Just a single week gets no number
            last_type = week.type
        except IndexError:  # Don't agonize over array bounds
            week.title = week.type.capitalize() + ' week'

        if week.variant == Week_variants.Rest:
            week.title += ' - Rest'

        for day in week.days:  # Set race week
            if day.date == form_data.race_date and week.title != 'Race week':  # Sometimes we already have a Race Week
                week.title += ' / Race week'

    plan.peak_week().title += ' / Peak week'


def apply_week_prototypes(plan, form_data):
    """ Apply the weekly prototype data to the individual days, e.g. distance, type. """
    for week in plan.weeks:
        try:
            week_proto = weeks.prototypes[week.type]
        except KeyError:
            logger.warn('Could not find key <{}> in Weekly prototypes. Using Base.'.format(week.type))
            week_proto = weeks.prototypes[Week_types.Base]

        for day in week.days:
            day_proto = week_proto[day.date.weekday()]  # e.g. Monday is 0
            day.distance = week._target_distance * day_proto['percent_of_weekly_distance']
            day_type = day_proto['type'].lower()
            try:
                day.type = {  # TODO: Convert types to actual. Is this pointless Java crap?
                    'rest': Day_types.Rest,
                    'recovery': Day_types.Recovery,
                    'easy': Day_types.Easy,
                    'quality': Day_types.Quality,
                    'long': Day_types.Long,
                    'crosstrain': Day_types.Crosstrain,
                }[day_type]
            except KeyError:
                logger.warn('Unknown day type <{}> in week proto <{}>'.format(day_type, week.type))
                day.type = Day_types.Easy  # Default

            if day.date == form_data.race_date:
                day.type = Day_types.Race


def assign_phases(plan, form_data):
    """ Mesocyles are applied backwards as time permits. """
    for i, week in enumerate(plan.weeks[::-1]):  # Work backwards
        if i < form_data.recovery_weeks:
            week.phase = Phases.Recovery
        elif i < form_data.recovery_weeks + 6:
            week.phase = Phases.Taper  # Taper & Race
        elif i < form_data.recovery_weeks + 12:
            week.phase = Phases.Prep  # Race Preparation
        elif i < form_data.recovery_weeks + 18:
            week.phase = Phases.Lactate  # Lactate Threshold
        else:
            week.phase = Phases.Base  # Base / Endurance


def assign_quality(plan, form_data):
    """ Turn day types into actual workouts. """
    for week in plan.weeks:
        for day in (x for x in plan.days if x.type == Day_types.Quality):
            try:
                workout_types = workouts.phases[week.phase]  # Choose workouts from current phase
            except KeyError:
                logging.error('Week phase <{}> not found in workout prototypes. Using Base.'.format(week.phase))
                workout_types = workouts.phases[Phases.Base]
            # TODO: Workout types from Enum
            type = random.choice(['Tempo', 'Intervals', 'Hills'])  # Pick a random type
            day.workout = random.choice(workout_types[type])  # Pick a random workout


def assign_daily_distances(plan, form_data):
    """ Now that weeks are set, customize individual daily distances. """
    for week in plan.weeks:
        for day in week.days:
            day.distance = min(day.distance, determine_max_long_run(form_data))  # Cap each day

            diff = week._target_distance - week.distance
            if diff > 5:
                short_day = week.shortest_day()
                if short_day.type == Day_types.Crosstrain:  # Usually the case
                    short_day.type = Day_types.Easy
                short_day.distance += diff   # A bit lame: shortest day gets bumped up. Be smarter than this?
            else:
                short_days = week.shortest_days(3)
                for day in short_days:
                    if day.type == Day_types.Crosstrain:
                        day.type = Day_types.Easy
                    day.distance += diff / 3  # Split equally

            if day.date == form_data.race_date:  # TODO: is there an easier way to find a specific date?
                day.distance = form_data.race_distance  # TODO: Split races up, based on pace, into multiple days



def determine_starting_mileage(form_data):
    return form_data.steady_mileage if form_data.steady_mileage is not None else 40


def determine_peak_mileage(form_data):
    return max(160, form_data.race_distance)


def determine_max_long_run(form_data):
    if form_data.race_distance <= 50:
        return 38  # ~ marathon training
    elif form_data.race_distance <= 80:
        return 42.2  # A full to make people feel good
    else:
        return 45


def generate_blank_plan(form_data):
    """
    A blank plan has all the days of training in it, including
    recovery block. But the no distances or workouts.
    """
    start_date = determine_plan_start(form_data.plan_start, int(form_data.week_day_start))  # TODO: Form Data Type conversion
    recovery_start = determine_recovery_start(form_data.race_date, start_date)
    end_date = add_recovery_block(recovery_start, form_data.recovery_weeks)
    all_dates = generate_plan_dates(start_date, end_date)
    all_days = list(Day(i, day) for i, day in enumerate(all_dates, start=1))
    all_weeks = list(Week(i, week) for i, week in enumerate(chunk_into_weeks(all_days), start=1))
    return Plan(form_data.race_name, all_weeks)


def determine_plan_start(plan_start, week_day_start):
    """
    Calculate when the plan's first day is, given that week 1 must start on
    the specified week_day_start.
    """
    diff = plan_start.weekday() - week_day_start
    delta_days = diff if diff >= 0 else 7 + diff
    return plan_start - datetime.timedelta(delta_days)


def needs_race_week(race_date, start_date):
    """ Calculate if we need to add a race week. """
    diff = race_date.weekday() - start_date.weekday()
    return 2 <= diff < 5  # Race is in the middle of the week


def determine_recovery_start(race_date, start_date):
    """
    Where race day falls in the week will determine whether it can be part
    of taper, recovery, or it's own 'race week'.
    """
    diff = race_date.weekday() - start_date.weekday()
    if 0 > diff > 7:
        logger.error('Diff value <{}> out of bounds'.format(diff))
        offset = 0
    if diff >= 5:  # Race is in last 2 days: Part of Taper
        offset = 7 - diff - 1  # Recovery starts after taper ends
    elif diff >= 2:  # Race is in the middle of the week: During a race week
        offset = 7 - diff - 1  # Recovery starts after race week ends
    else:  # Race is part of Recovery week 1
        offset = -diff - 1  # Recovery block starts after taper ends
    return race_date + relativedelta(days=offset)


def add_recovery_block(recovery_start, recovery_weeks):
    return recovery_start + relativedelta(weeks=+recovery_weeks)


def generate_plan_dates(start, end):
    return list(d.date() for d in rrule(DAILY, dtstart=start, until=end))


def chunk_into_weeks(seq, size=7):
    """ Chunks days into week batches. """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
