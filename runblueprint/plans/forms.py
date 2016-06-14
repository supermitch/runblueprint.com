from django import forms


WEEKDAYS = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]


class PlanForm(forms.Form):
    # Race details
    race_date = forms.DateField()
    race_distance = forms.IntegerField()
    race_units = forms.ChoiceField(label='Units', choices=[('mi', 'mi'), ('km', 'km')])
    race_terrain = forms.ChoiceField(choices=[
        ('flat', 'flat'), ('hilly', 'hilly'), ('mountain', 'mountain')
    ])
    expected_time = forms.TimeField(label='Expected completion time')

    # Running ability
    steady_mileage = forms.IntegerField()
    peak_mileage = forms.IntegerField()
    year_mileage = forms.IntegerField(label='Total year mileage')
    three_month_mileage = forms.IntegerField()

    # TODO: longest distance & time
    longest_distance = forms.IntegerField(label='Longest distance')
    longest_distance_units = forms.ChoiceField(label='Units', choices=[('mi', 'mi'), ('km', 'km')])
    ten_km_pr = forms.TimeField(label='10k PR')
    your_name = forms.CharField()

    # Schedule
    plan_start = forms.DateField(label='Training start date')
    week_day_start = forms.ChoiceField(choices=WEEKDAYS)
    long_run_day = forms.ChoiceField(choices=[('Saturday', 'Saturday'), ('Sunday', 'Sunday')])
    days_off = forms.MultipleChoiceField(choices=WEEKDAYS)
    double_days = forms.MultipleChoiceField(choices=WEEKDAYS)
    crosstraining_days = forms.MultipleChoiceField(choices=WEEKDAYS)

