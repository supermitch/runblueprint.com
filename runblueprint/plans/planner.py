import collections
import datetime
import logging
import math
import uuid

from dateutil.relativedelta import *
from dateutil.rrule import *

from plans.prototypes import weeks


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)


class Plan():
    def __init__(self, name, weeks):
        self.name = name
        self.id = uuid.uuid1().hex
        self.weeks = weeks  # List of weeks

    def __str__(self):
        return '{} {} Week Plan'.format(self.name, len(self.weeks))

    @property
    def distance(self):
        return sum(x.distance for x in self.weeks)

    @property
    def time(self):
        return sum(x.time for x in self.weeks)

    @property
    def days(self):
        """ A handy generator of all plan days. """
        return (day for week in self.weeks for day in week.days)


    def get_by_title(self, title):
        """ Find a week by title, return (index, week) tuple. """
        for i, week in enumerate(self.weeks):
            if week.title.lower() == title:
                return i, week

    def count_weeks_by_type(self, type):
        """ Count number of weeks for a given type. """
        return sum(1 for x in self.weeks if x.type == getattr(Week.Types, type))

    def get_weeks_by_type(self, type):
        """ Return list of (index, week) tuples of weeks of a given type. """
        return [(i, x) for i, x in enumerate(self.weeks) if x.type == type]

    def get_day_by_date(self, date):
        for week in self.weeks:
            for day in week.days:
                if day.date == date:
                    return day


class Week():
    WeekTypes = ('Base', 'Growth', 'Work', 'Taper', 'Race', 'Recovery')
    Types = collections.namedtuple('WeekTypes', WeekTypes)(*WeekTypes)  # Define constants for types

    Variants = collections.namedtuple('Variants', ('Rest',))(('Rest',))  # Define variants

    def __init__(self, number, days):
        self.number = number
        self.days = days  # List of days
        self.title = ''
        self.type = ''
        self.variant = ''
        self._target_distance = 0  # Internal: planned distance for that week

    @property
    def distance(self):
        return sum(day.distance for day in self.days)

    @property
    def time(self):
        return sum(day.time for day in self.days)

    def __str__(self):
        return 'Week {}: {} - {:.1f} km'.format(self.number, self.title, self.distance)


class Day():
    DayTypes = ('Recovery', 'Easy', 'Long', 'Quality', 'Rest', 'Crosstrain')
    Types = collections.namedtuple('DayTypes', DayTypes)(*DayTypes)  # Define constants types

    def __init__(self, number, date):
        self.number = number
        self.date = date
        self.distance = 0
        self.time = 0
        self.type = ''  # Run type, e.g. Easy, Tempo

    def __str__(self):
        return '{}. {} {}: {} {:.1f}'.format(self.number, self.date.strftime('%Y-%m-%d'),
            self.date.strftime('%a'), self.type, self.distance)



def generate_plan(form_data):
    plan = generate_blank_plan(form_data)

    assign_week_types(plan, form_data)
    assign_week_titles(plan, form_data)
    assign_weekly_distance(plan, form_data)
    apply_week_prototypes(plan, form_data)
    assign_daily_distances(plan, form_data)

    return plan


def assign_week_types(plan, form_data):
    for i, week in enumerate(plan.weeks[::-1]):  # Work backwards
        if i < form_data.recovery_weeks:
            week.type = Week.Types.Recovery
        elif i < form_data.recovery_weeks + form_data.taper_length:
            week.type = Week.Types.Taper
        elif i < form_data.recovery_weeks + form_data.taper_length + 18:
            week.type = Week.Types.Work
        else:
            week.type = Week.Types.Base


def assign_week_titles(plan, form_data):
    """ Turn types into titles. """
    counter = 0
    last_type = None
    for i, week in enumerate(plan.weeks):
        try:
            if week.type == last_type:  # If this week type is the same as the last
                counter += 1
                week.title = '{} week {}'.format(week.type.capitalize(), counter)
            else:  # It's a new type, or the first week
                counter = 1
                if week.type == plan.weeks[i + 1].type:  # Only add a 1 if next week is a 2!
                    week.title = week.type.capitalize() + ' week 1'
                else:
                    week.title = week.type.capitalize() + ' week'  # Just a single week gets no number
            last_type = week.type
        except IndexError:  # Don't agonize over array bounds
            week.title = week.type.capitalize() + ' week'

        if (i + 1) % 4 == 0:  # Every 4th week is a rest week
            if week.type in (Week.Types.Base, Week.Types.Work):  # Other phases have no rest weeks
                week.variant = Week.Variants.Rest
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
        if week.variant == Week.Variants.Rest:
            target_distance *= 0.6  # Rest week is 60 %
        week._target_distance = target_distance

    # Set taper volumes
    taper_count = plan.count_weeks_by_type(Week.Types.Taper)
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

    for idx, (i, week) in enumerate(plan.get_weeks_by_type(Week.Types.Taper), start=1):
        taper_percent = taper_percents[idx]
        week._target_distance = taper_percent * peak_dist

    for idx, (i, week) in enumerate(plan.get_weeks_by_type(Week.Types.Recovery), start=1):
        recovery_percent = {1: 0.20, 2: 0.36, 3: 0.43, 4: 0.50, 5: 0.59}[idx]
        week._target_distance = recovery_percent * peak_dist


def apply_week_prototypes(plan, form_data):
    """ Apply the weekly prototype data to the individual days, e.g. distance, type. """
    for week in plan.weeks:
        try:
            week_proto = weeks.prototypes[week.type]
        except KeyError:
            logger.warn('Could not find key <{}> in Weekly prototypes. Using Base.'.format(week.type))
            week_proto = weeks.prototypes[Week.Types.Base]

        for day in week.days:
            day_proto = week_proto[day.date.weekday()]  # e.g. Monday is 0
            day.distance = week._target_distance * day_proto['percent_of_weekly_distance']
            day_type = day_proto['type'].lower()
            day.type = {  # Convert types to actual. Is this pointless Java crap?
                'rest': Day.Types.Rest,
                'recovery': Day.Types.Recovery,
                'easy': Day.Types.Easy,
                'quality': Day.Types.Quality,
                'long': Day.Types.Long,
                'x-train': Day.Types.Crosstrain,
            }.get(day_type, Day.Types.Easy)  # Default to Easy on err. TODO: Try-except-log

            if day.date == form_data.race_date:
                day.type = 'Race!'


def assign_quality(plan, form_data):
    """ Turn day types into actual workouts. """
    for day in plan.days:
        if day.type == Day.Types.Quality:
            # TODO: Do we need to know phases of the plan?
            day.workout = 'What am I doing?'


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
    end_date = add_recovery_block(form_data.race_date, form_data.recovery_weeks)
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


def add_recovery_block(race_date, recovery_weeks):
    return race_date + relativedelta(weeks=+recovery_weeks)


def generate_plan_dates(start, end):
    return list(d.date() for d in rrule(DAILY, dtstart=start, until=end))


def chunk_into_weeks(seq, size=7):
    """ Chunks days into week batches. """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))
