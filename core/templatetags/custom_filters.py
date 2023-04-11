from django import template

register = template.Library()


# Устанавливает атрибут class виджета
@register.filter
def add_class(field, classes):
    try:
        field.field.widget.attrs['class'] = classes
    except AttributeError:
        return field
    return field


# Устанавливает значение field.initial
@register.filter
def set_initial_value(field, value):
    if hasattr(field, 'initial'):
        field.initial = value
    return field


@register.filter
def set_id(field, element_id):
    try:
        field.field.widget.attrs['id'] = element_id
    except AttributeError:
        return field
    return field
