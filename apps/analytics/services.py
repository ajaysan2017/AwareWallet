from django.db.models import Sum, Avg, Max, Count
from django.utils import timezone
from apps.transactions.models import Transaction


def get_monthly_summary(user, year=None, month=None):
    today = timezone.now().date()
    year = year or today.year
    month = month or today.month

    qs = Transaction.objects.filter(
        user=user, date__year=year, date__month=month
    )
    income = qs.filter(type='income').aggregate(t=Sum('amount'))['t'] or 0
    expenses = qs.filter(type='expense').aggregate(t=Sum('amount'))['t'] or 0
    return {
        'income': income,
        'expenses': expenses,
        'balance': income - expenses,
        'transaction_count': qs.count(),
    }


def get_top_spending_categories(user, year=None, month=None, limit=5):
    today = timezone.now().date()
    year = year or today.year
    month = month or today.month

    return Transaction.objects.filter(
        user=user, type='expense',
        date__year=year, date__month=month
    ).values(
        'category__name', 'category__color'
    ).annotate(
        total=Sum('amount')
    ).order_by('-total')[:limit]


def get_average_daily_spending(user, year=None, month=None):
    today = timezone.now().date()
    year = year or today.year
    month = month or today.month

    result = Transaction.objects.filter(
        user=user, type='expense',
        date__year=year, date__month=month
    ).aggregate(avg=Avg('amount'))
    return round(result['avg'] or 0, 2)


def get_largest_transaction(user, year=None, month=None):
    today = timezone.now().date()
    year = year or today.year
    month = month or today.month

    return Transaction.objects.filter(
        user=user, type='expense',
        date__year=year, date__month=month
    ).select_related('category').order_by('-amount').first()


def get_monthly_comparison(user, months=6):
    """Returns income vs expense for last N months."""
    from dateutil.relativedelta import relativedelta
    today = timezone.now().date()
    results = []

    for i in range(months - 1, -1, -1):
        target = today - relativedelta(months=i)
        year = target.year
        month = target.month
        summary = get_monthly_summary(user, year, month)
        summary['month'] = target.strftime('%b %Y')
        results.append(summary)

    return results