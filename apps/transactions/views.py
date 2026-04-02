"""
Transaction views for AwareWallet.
 
Handles dashboard, transaction listing, creation, updating and deletion.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Transaction
from .forms import TransactionForm
from .filters import TransactionFilter
from apps.budgets.models import Budget


@login_required
def dashboard(request):
    today = timezone.now().date()
    transactions = Transaction.objects.filter(user=request.user)

    # Monthly totals
    monthly = transactions.filter(date__year=today.year, date__month=today.month)
    income = monthly.filter(type='income').aggregate(t=Sum('amount'))['t'] or 0
    expenses = monthly.filter(type='expense').aggregate(t=Sum('amount'))['t'] or 0
    balance = income - expenses

    # Budget alerts
    budgets = Budget.objects.filter(
        user=request.user,
        month__year=today.year,
        month__month=today.month
    )
    alerts = [b for b in budgets if b.alert_level in ('warning', 'danger', 'exceeded')]

    # Recent transactions
    recent = transactions.select_related('category')[:5]

    return render(request, 'dashboard.html', {
        'income': income,
        'expenses': expenses,
        'balance': balance,
        'alerts': alerts,
        'recent_transactions': recent,
        'today': today,
        'transaction_count': monthly.count(),
    })


@login_required
def transaction_list(request):
    qs = Transaction.objects.filter(user=request.user).select_related('category')
    f = TransactionFilter(request.GET, queryset=qs, request=request)
    return render(request, 'transactions/list.html', {'filter': f})


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            t = form.save(commit=False)
            t.user = request.user
            t.type = form.cleaned_data['type']  
            t.save()
            messages.success(request, 'Transaction added!')
            return redirect('transaction-list')
    else:
        form = TransactionForm(request.user)
    return render(request, 'transactions/form.html', {'form': form, 'action': 'Add'})


@login_required
def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST, instance=transaction)
        if form.is_valid():
            t = form.save(commit=False)
            t.type = form.cleaned_data['type']  
            t.save()
            messages.success(request, 'Transaction updated!')
            return redirect('transaction-list')
    else:
        form = TransactionForm(request.user, instance=transaction)
    return render(request, 'transactions/form.html', {'form': form, 'action': 'Update'})

@login_required
def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted.')
        return redirect('transaction-list')
    return render(request, 'transactions/confirm_delete.html', {'object': transaction})
