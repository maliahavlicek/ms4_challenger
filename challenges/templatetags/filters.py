from django import template
from datetime import datetime
from collections.abc import Iterable
from decimal import Decimal

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
    """function expects an array of dictionaries of Entry type, loops through and tries to match to provided User in match"""
    if isinstance(value, Iterable):
        for entry in value:
            if entry.user and entry.user == match:
                return entry
        else:
            return False
    else:
        return False


@register.filter(name="percent_rating")
def percent_rating(value):
    """take rating value and divide by 3 return decimal percentage value"""
    value = Decimal(value)
    value = round(value / 3, 2) * 100
    return value


@register.filter(name="num")
def num(value):
    """take rating value and divide by 3 return decimal percentage value"""
    value = Decimal(value)
    return value


@register.inclusion_tag("challenges/video_player.html", takes_context=False)
def vid_player(video_url, id=None, width='100%', height='auto'):
    """ take url value and does dynamic html for a video player"""
    return {'video_url': video_url, 'width': width, 'height': height, 'id': id }
