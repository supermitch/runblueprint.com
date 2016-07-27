class FormData():
    """
    An object to act as an interface between the form
    data and the planner.
    """
    def __init__(self, raw_form_data):
        """ Take cleaned Django form data, save it, and assign it as attrs. """
        self.raw_data = raw_form_data
        print(self.raw_data)
        self.parse_raw_data()

    def parse_raw_data(self):
        """ Turn dict k:v pairs into instance attributes """
        ints = [
            'race_distance',
            'steady_mileage',
            'peak_mileage',
            'year_mileage',
            'three_month_mileage',
            'longest_distance',
            'taper_length',
            'recovery_weeks',
        ]
        for key, value in self.raw_data.items():
            if value is not None and key in ints:
                value = int(value)
            setattr(self, key, value)
