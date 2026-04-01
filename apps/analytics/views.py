"""Analytics views for AwareWallet."""
from django.shortcuts import render
from apps.users.templatetags.currency_filters import CURRENCY_SYMBOLS
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
import json
from .services import (
    get_monthly_summary,
    get_top_spending_categories,
    get_average_daily_spending,
    get_largest_transaction,
    get_monthly_comparison,
)


@login_required
def analytics_dashboard(request):
    today = timezone.now().date()
    user = request.user
    monthly = get_monthly_comparison(user)
    symbol = CURRENCY_SYMBOLS.get(user.currency.upper(), user.currency)

    context = {
        'summary': get_monthly_summary(user),
        'top_categories': list(get_top_spending_categories(user)),
        'avg_daily': get_average_daily_spending(user),
        'largest_tx': get_largest_transaction(user),
        'monthly_comparison': json.dumps(monthly, cls=DjangoJSONEncoder),
        'currency_symbol': symbol,
        'today': today,
    }
    return render(request, 'analytics/dashboard.html', context)
