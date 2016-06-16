import datetime

from django import forms


UNITS = [('mi', 'mi'), ('km', 'km')]
TERRAINS = [('flat', 'flat'), ('hilly', 'hilly'), ('mountain', 'mountain')]
WEEKENDS = [('Saturday', 'Saturday'), ('Sunday', 'Sunday')]
WEEKDAYS = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]
TAPER_LENGTHS = [('1 week', '1 week'), ('2 weeks', '2 weeks'), ('3 weeks', '3 weeks')]


class PlanForm(forms.Form):

    # Other
    your_name = forms.CharField()

    # Race details
    race_date = forms.DateField(help_text='yyyy-mm-dd')
    race_distance = forms.IntegerField()
    race_units = forms.ChoiceField(label='Units', choices=UNITS)
    race_terrain = forms.ChoiceField(choices=TERRAINS,
        widget=forms.RadioSelect)
    expected_time = forms.CharField(label='Expected completion time',
        help_text='e.g. 23:59:59')

    # Running ability
    steady_mileage = forms.IntegerField()
    peak_mileage = forms.IntegerField()
    year_mileage = forms.IntegerField(label='Total year mileage')
    three_month_mileage = forms.IntegerField()

    longest_distance = forms.IntegerField(label='Longest distance')
    # TODO: Longest distance duration
    longest_distance_units = forms.ChoiceField(label='Units',
        choices=UNITS,
        widget=forms.RadioSelect)
    ten_km_pr = forms.CharField(label='10k PR',
        help_text='e.g. 38:27')

    # Schedule
    plan_start = forms.DateField(label='Training start date',
        initial=datetime.date.today)
    week_day_start = forms.ChoiceField(choices=WEEKDAYS,
        initial=WEEKDAYS[0][0])
    long_run_day = forms.ChoiceField(choices=WEEKENDS,
        initial=WEEKENDS[0][0],
        widget=forms.RadioSelect)
    days_off = forms.MultipleChoiceField(choices=WEEKDAYS,
        initial=(WEEKDAYS[4][0],),
        widget=forms.CheckboxSelectMultiple)
    double_days = forms.MultipleChoiceField(choices=WEEKDAYS,
        initial=(WEEKDAYS[0][0], WEEKDAYS[3][0]),
        widget=forms.CheckboxSelectMultiple)
    crosstraining_days = forms.MultipleChoiceField(choices=WEEKDAYS,
        initial=(WEEKDAYS[1][0],),
        widget=forms.CheckboxSelectMultiple)
    taper_length = forms.ChoiceField(choices=TAPER_LENGTHS,
        initial=TAPER_LENGTHS[1][0],
        widget=forms.RadioSelect)

