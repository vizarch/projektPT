from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def pretty_list(value, arg):
    result = []
    for tmp in value.split(","):
        if tmp[0] == " ":
            tmp = tmp[1:]
        result.append(tmp)
    result = arg.join(result)
    return result
