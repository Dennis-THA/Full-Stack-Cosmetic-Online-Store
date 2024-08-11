from django import template

register = template.Library()

@register.filter
def star_rating(rating):
    # Generate a list of star statuses (filled or empty)
    filled_stars = ['ri-star-fill'] * rating
    empty_stars = ['ri-star-line'] * (5 - rating)
    return filled_stars + empty_stars