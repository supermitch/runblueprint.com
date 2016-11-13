from dateutil.relativedelta import *


class FormData():
    """
    An object to act as an interface between the raw form
    data and the planner.
    """
    def __init__(self, raw_form_data):
        """ Take cleaned Django form data, save it, and assign it as attrs. """
        self.parse_raw_data(raw_form_data)

    def parse_raw_data(self, raw_data):
        """ Turn dict k:v pairs into instance attributes """
        ints = [  # List of integer attributes
            'longest_distance',
            'peak_mileage',
            'race_distance',
            'recovery_weeks',
            'steady_mileage',
            'taper_length',
            'three_month_mileage',
            'week_day_start',
            'year_mileage',
        ]
        for key, value in raw_data.items():
            if key in ints and value is not None:
                value = int(value)
            setattr(self, key, value)
