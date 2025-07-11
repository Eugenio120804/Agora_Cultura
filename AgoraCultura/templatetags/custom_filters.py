from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Moltiplica il valore per l'argomento"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''
