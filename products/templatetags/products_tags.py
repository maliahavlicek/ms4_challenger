from django.utils.safestring import mark_safe
from django import template
import decimal

register = template.Library()


@register.filter()
def format_price(price):
    """
    Outputs a formatted price object.
    """
    if isinstance(price, decimal.Decimal):
        if price == 0.00:
            content = '<span class="dollar-symbol">Free</span>'
            return mark_safe(content)

        # split string on period, price comes for a decimal field with 2 decimal fields so it will always have .xx
        items = str(price).split('.')
        dollars = "0"
        cents = "00"
        if len(items) > 1:
            if len(items[0]) > 0:
                dollars = items[0]
                cents = items[1]

        content = '<span class="dollar-symbol">$</span><class="dollars">' + dollars + '</span>.<span class="cents">' + cents + '</span>'
        return mark_safe(content)
    else:
        return price
