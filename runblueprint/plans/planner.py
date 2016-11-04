import collections
import datetime
import enum
import logging
import math

from dateutil.relativedelta import *
from dateutil.rrule import *

from plans.week import Week, Week_types, Week_variants
from plans.plan import Plan, Phases
from plans.day import Day, Day_types
from plans.prototypes import weeks


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


def generate_plan(form_data):
    plan = generate_blank_plan(form_data)

    assign_phases(plan, form_data)
    assign_week_types(plan, form_data)
    assign_week_titles(plan, form_data)
    assign_weekly_distance(plan, form_data)
    apply_week_prototypes(plan, form_data)
    assign_quality(plan, form_data)
    assign_daily_distances(plan, form_data)

    return plan


def assign_week_types(plan, form_data):
    race_week = needs_race_week(form_data.race_date, form_data.start_date)
    race_week_count = 1 if race_week else 0
    for i, week in enumerate(plan.weeks[::-1]):  # Work backwards
        if i < form_data.recovery_weeks:
            week.type = Week_types.Recovery
        elif race_week and i < form_data.recovery_weeks + race_week_count:
            week.type = Week_types.Race
        elif i < form_data.recovery_weeks + race_week_count + form_data.taper_length:
            week.type = Week_types.Taper
        elif i < form_data.recovery_weeks + race_week_count + form_data.taper_length + 18:
            week.type = Week_types.Work
        else:
            week.type = Week_types.Base


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

        if (i + 1) % 4 == 0:  # Every 4th week is a rest week
            if week.type in (Week_types.Base, Week_types.Work):  # Other phases have no rest weeks
                week.variant = Week_variants.Rest
                week.title += ' - Rest'

        for day in week.days:  # Set peak & race week
            if day.date == form_data.peak_day:
                week.title = 'Peak week'
            elif day.date == form_data.race_date:
                week.title = 'Race week'


def assign_weekly_distance(plan, form_data):
    """ Assign weekly mileage targets to each of our plan's weeks. """
    start_dist = determine_starting_mileage(form_data)  # TODO: Week 0 might be a base phase and not actually use the "starting mileage" value
    peak_dist = determine_peak_mileage(form_data)

    start_idx = 0
    peak_idx, _ = plan.get_by_title('peak week')

    # Set work volumes
    # TODO: set distances differently for base & work phases
    for i, week in enumerate(plan.weeks[:peak_idx + 1]):  # Fill in from weeks 0 to peak week, inclusive
        target_distance = start_dist + (peak_dist - start_dist) / (peak_idx - start_idx) * i  # Linearly increase in mileage from start to peak
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
            week.phase = Phases.Recovery  # TODO: Redundant with week type?
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
    for day in plan.days:
        if day.type == Day_types.Quality:
            # TODO: decide phases of the plan
            day.workout = 'warmup + workout + cooldown'


def assign_daily_distances(plan, form_data):
    """ Now that weeks are set, customize individual daily distances. """
    for day in plan.days:
        day.distance = min(day.distance, determine_max_long_run(form_data))
        # TODO: Now we need to redo the other run distances
        if day.date == form_data.race_date:  # TODO: is there an easier way to find a specific date?
            day.distance = form_data.race_distance


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
    recovery_start = determine_race_week(form_data.race_date, start_date)
    end_date = add_recovery_block(recovery_start, form_data.recovery_weeks)
    all_dates = generate_plan_dates(start_date, end_date)
    all_days = list(Day(i, d) for i, d in enumerate(all_dates, start=1))
    all_weeks = list(Week(i, w) for i, w in enumerate(chunk_into_weeks(all_days), start=1))
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
    return 2 <= diff <= 5  # Race is in the middle of the week


def determine_race_week(race_date, start_date):
    """
    Where race day falls in the week will determine whether it can be part
    of taper, recovery, or it's own 'race week'.
    """
    diff = race_date.weekday() - start_date.weekday()
    if 0 < diff > 7:
        logger.warn('Diff value <{}> out of bounds'.format(diff))
        recovery_start = race_date
    if diff >= 5:  # Race is in last 2 days
        print('Race during taper')
        # Race day is part of taper week. Recovery starts after taper ends
        recovery_start = race_date + relativedelta(days=+diff)
    elif diff >= 2:  # Race is in the middle of the week
        print('Must add race week')
        # We need to add a race week. Recovery starts after race week ends
        recovery_start = race_date + relativedelta(days=+diff)
    else:  # Race is part of Recovery week 1
        print('Race during Recovery')
        recovery_start = race_date + relativedelta(days=-diff)  # Recovery block starts after taper ends
    print(recovery_start)
    return recovery_start


def add_recovery_block(recovery_start, recovery_weeks):
    return recovery_start + relativedelta(weeks=+recovery_weeks)


def generate_plan_dates(start, end):
    return list(d.date() for d in rrule(DAILY, dtstart=start, until=end))


def chunk_into_weeks(seq, size=7):
    """ Chunks days into week batches. """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
