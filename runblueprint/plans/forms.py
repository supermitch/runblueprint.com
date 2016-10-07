import datetime

from django import forms

from . import date_utils


UNITS = [('mi', 'mi'), ('km', 'km')]
TERRAINS = [('flat', 'flat'), ('hilly', 'hilly'), ('mountain', 'mountain')]
WEEKENDS = [('Saturday', 'Saturday'), ('Sunday', 'Sunday')]
WEEKDAYS = [
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
]
TAPER_LENGTHS = [('1 week', '1 week'), ('2 weeks', '2 weeks'), ('3 weeks', '3 weeks')]


class PlanForm(forms.Form):

    # Other
    your_name = forms.CharField(required=False)

    # Race details
    race_date = forms.DateField(initial=date_utils.six_months,
        help_text='(yyyy-mm-dd)')
    race_distance = forms.IntegerField(initial=100)

    # Running ability
    steady_mileage = forms.IntegerField(initial=40, required=False,
            help_text='Weekly mileage you could handle without overuse injuries')

    # Schedule
    plan_start = forms.DateField(label='Training start date',
        help_text='(yyyy-mm-dd)',
        initial=datetime.date.today)
    week_day_start = forms.ChoiceField(choices=WEEKDAYS,
        initial=WEEKDAYS[0][0],
        required=False,
        disabled=True)
    taper_length = forms.IntegerField(initial=3,
        required=False,
        help_text='We recommend 2 or 3 weeks')
    recovery_weeks = forms.IntegerField(initial=5,
        required=False,
        help_text='We recommend between 5 and 8 weeks')

