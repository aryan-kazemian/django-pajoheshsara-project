from django import template
import jalali_date

register = template.Library()

@register.filter(name='three_digits_currency')
def three_digits_currency(value: int):
    value = int(value)
    return '{:,}'.format(value) + ' تومان'

@register.filter(name='jalali_date')
def jalali(date):
    return jalali_date.date2jalali(date)


