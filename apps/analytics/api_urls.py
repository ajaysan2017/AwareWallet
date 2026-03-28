from django.urls import path
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import (
    get_monthly_summary,
    get_top_spending_categories,
    get_average_daily_spending,
    get_largest_transaction,
    get_monthly_comparison,
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def insights(request):
    user = request.user
    largest = get_largest_transaction(user)

    # Extract nested conditional into independent statement
    if largest and largest.category:
        category_name = largest.category.name
    else:
        category_name = None

    # Build largest transaction dict separately
    if largest:
        largest_transaction_data = {
            'amount': largest.amount,
            'description': largest.description,
            'date': largest.date,
            'category': category_name,
        }
    else:
        largest_transaction_data = None

    return Response({
        'summary': get_monthly_summary(user),
        'top_categories': list(get_top_spending_categories(user)),
        'avg_daily_spending': get_average_daily_spending(user),
        'largest_transaction': largest_transaction_data,
        'monthly_comparison': get_monthly_comparison(user),
    })


urlpatterns = [
    path('insights/', insights, name='api-insights'),
]