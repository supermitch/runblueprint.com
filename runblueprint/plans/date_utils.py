from datetime import date
from dateutil.relativedelta import relativedelta


def six_months(initial_date=None):
    initial_date = date.today() if initial_date is None else initial_date
    return initial_date + relativedelta(months=+6)
