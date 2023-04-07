from django import template

register = template.Library()


# Устанавливает атрибут class виджета
@register.filter
def add_class(field, classes):
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={'class': classes})
    return field


# Устанавливает значение атрибута value виджета
@register.filter
def set_value(field, value):
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={'value': value})
    return field
