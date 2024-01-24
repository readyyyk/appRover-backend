from datetime import date, datetime


def check_deadline(_date: date):
    assert _date > datetime.now().date(), 'Date must be greater than current date'
    return _date
