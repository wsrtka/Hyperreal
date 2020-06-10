import re
from datetime import date, timedelta


def parse_date(date_string):
    """
    Parse date from hyperreal.info format into python date
    :param date_string: date string, as found at the hyperreal.info forum
    :return: parsed date
    """
    if 'dzisiaj' in date_string or 'temu' in date_string:
        result = date.today()
    elif 'wczoraj' in date_string:
        result = date.today() - timedelta(1)
    else:
        date_match = re.compile(r'([0-9]{1,2}) ([a-ząęćńłżźóś]+) ([0-9]{4})').match(date_string)
        result = date(year=int(date_match.group(3)), month=_get_month(date_match.group(2)),
                      day=int(date_match.group(1)))
    return result


def _get_month(month_string):
    dates = {
        'stycznia': 1,
        'lutego': 2,
        'marca': 3,
        'kwietnia': 4,
        'maja': 5,
        'czerwca': 6,
        'lipca': 7,
        'sierpnia': 8,
        'września': 9,
        'października': 10,
        'listopada': 11,
        'grudnia': 12
    }
    if month_string in dates:
        return dates[month_string]
    return None
