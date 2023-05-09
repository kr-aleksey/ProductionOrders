from django import template

register = template.Library()


# Устанавливает атрибут class виджета
@register.filter
def add_class(value, arg):
    try:
        value.field.widget.attrs['class'] = arg
    except AttributeError:
        pass
    return value


# Устанавливает обработчик события onchange виджета
@register.filter
def onchange(value, arg):
    try:
        value.field.widget.attrs['onchange'] = arg
    except AttributeError:
        pass
    return value


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
