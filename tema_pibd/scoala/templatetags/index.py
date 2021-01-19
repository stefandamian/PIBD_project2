from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def nume(obj):
    return obj.nume

@register.filter
def prenume(obj):
    return obj.prenume

@register.filter
def an(obj):
    return obj.an

@register.filter
def profesor(obj):
    return obj.profesor
