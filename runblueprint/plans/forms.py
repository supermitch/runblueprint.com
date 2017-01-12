import datetime

from django import forms

from . import date_utils


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


class PlanForm(forms.Form):

    # Other
    race_name = forms.CharField(required=False)

    # Units
    UNITS = [('mi', 'miles'), ('km', 'kilometres')]
    units = forms.ChoiceField(choices=UNITS, widget=forms.RadioSelect(), initial='mi', required=True,
        label='Distance units',
        help_text='Units for all measurements')

    # Race details
    race_date = forms.DateField(initial=date_utils.six_months, required=True,
        help_text='(yyyy-mm-dd)')
    race_distance = forms.IntegerField(initial=100, required=True,
        label='Race distance')

    # Running ability
    steady_mileage = forms.IntegerField(initial=40, required=False,
        help_text='Weekly mileage you could handle without overuse injuries')

    # Schedule
    plan_start = forms.DateField(initial=datetime.date.today, required=True,
        label='Training start date',
        help_text='(yyyy-mm-dd)')
    week_day_start = forms.ChoiceField(choices=WEEKDAYS, initial=WEEKDAYS[0][0], required=True)

    taper_length = forms.IntegerField(initial=3, required=False,
        help_text='We recommend 2 or 3 weeks')
    recovery_weeks = forms.IntegerField(initial=5, required=False,
        help_text='We recommend between 5 and 8 weeks')

    # Training options
    growth_methods = [('step','Daniels (monthly)'), ('gradual','Gradual (weekly)')]
    growth_method = forms.ChoiceField(choices=growth_methods, widget=forms.RadioSelect(), initial='step')
