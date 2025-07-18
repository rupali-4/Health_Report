# reports/templatetags/querystring.py

from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def querystring(context, *args):
    """
    Preserves the existing query parameters, except the ones passed in *args.
    This is useful for pagination and exporting filters.
    """
    request = context['request']
    query = request.GET.copy()
    for arg in args:
        query.pop(arg, None)
    return query.urlencode()
