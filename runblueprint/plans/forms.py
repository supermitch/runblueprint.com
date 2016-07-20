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
    race_date = forms.DateField(help_text='yyyy-mm-dd',
        initial=date_utils.six_months)
    race_distance = forms.IntegerField(initial=100)
    race_units = forms.ChoiceField(label='Units', choices=UNITS,
        initial=WEEKENDS[0][0])
    race_terrain = forms.ChoiceField(choices=TERRAINS,
        initial=TERRAINS[1][0],
        widget=forms.RadioSelect)
    expected_time = forms.CharField(label='Expected completion time',
        required=False,
        help_text='e.g. 23:59:59')

    # Running ability
    steady_mileage = forms.IntegerField(required=False)
    peak_mileage = forms.IntegerField(required=False)
    year_mileage = forms.IntegerField(label='Total year mileage',
        required=False)
    three_month_mileage = forms.IntegerField(
        required=False)

    longest_distance = forms.IntegerField(label='Longest distance',
        required=False)
    # TODO: Longest distance duration
    longest_distance_units = forms.ChoiceField(label='Units',
        choices=UNITS,
        initial=WEEKENDS[0][0])
    ten_km_pr = forms.CharField(label='10k PR',
        help_text='e.g. 38:27',
        required=False)
    # Schedule
    plan_start = forms.DateField(label='Training start date',
        initial=datetime.date.today)
    week_day_start = forms.ChoiceField(choices=WEEKDAYS,
        initial=WEEKDAYS[0][0],
        required=False)
    long_run_day = forms.ChoiceField(choices=WEEKENDS,
        initial=WEEKENDS[0][0],
        widget=forms.RadioSelect,
        required=False)
    days_off = forms.MultipleChoiceField(choices=WEEKDAYS,
        initial=(WEEKDAYS[4][0],),
        widget=forms.CheckboxSelectMultiple,
        required=False)
    double_days = forms.MultipleChoiceField(choices=WEEKDAYS,
        initial=(WEEKDAYS[0][0], WEEKDAYS[3][0]),
        widget=forms.CheckboxSelectMultiple,
        required=False)
    crosstraining_days = forms.MultipleChoiceField(choices=WEEKDAYS,
        initial=(WEEKDAYS[1][0],),
        widget=forms.CheckboxSelectMultiple,
        required=False)
    taper_length = forms.ChoiceField(choices=TAPER_LENGTHS,
        initial=TAPER_LENGTHS[2][0],
        widget=forms.RadioSelect)
    recovery_weeks = forms.IntegerField(initial=5,
        required=False,
        help_text='We recommend between 5 and 8 weeks')

