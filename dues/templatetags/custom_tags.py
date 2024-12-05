from django import template

register = template.Library()

@register.filter
def year_range(start_year, end_year):
    return range(start_year, end_year + 1)