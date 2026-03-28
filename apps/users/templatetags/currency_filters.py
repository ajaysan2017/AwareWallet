from django import template

register = template.Library()

CURRENCY_SYMBOLS = {
    'USD': '$',
    'EUR': '€',
    'GBP': '£',
    'INR': '₹',
    'JPY': '¥',
    'CAD': 'CA$',
    'AUD': 'A$',
    'CHF': 'Fr',
    'CNY': '¥',
    'SEK': 'kr',
    'NOK': 'kr',
    'MXN': 'MX$',
    'SGD': 'S$',
    'AED': 'د.إ',
}

@register.simple_tag(takes_context=True)
def currency_symbol(context):
    request = context.get('request')
    if request and request.user.is_authenticated:
        code = request.user.currency.upper()
        return CURRENCY_SYMBOLS.get(code, code)
    return '$'
