from django import template
from datetime import datetime
from collections.abc import Iterable
register = template.Library()


@register.filter()
def format_date(date):
    """Function takes a datetime object and stringifies it down to MM/DD/YYYY format"""
    try:
        start_date = datetime.strftime(date, '%m/%d/%Y')
    except (TypeError, ValueError) as e:
        start_date = date
        pass
    return start_date


@register.filter(name='has_user')
def has_user(value, match):
    """function expects an array of dictionaries with a key of user and searches for match on value"""
    if isinstance(value, Iterable):
        for item in value:
            if item.user and item.user == match:
                return True
        else:
            return False
    else:
        return False
