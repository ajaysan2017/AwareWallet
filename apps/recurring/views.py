from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RecurringTransaction
from .forms import RecurringTransactionForm


@login_required
def recurring_list(request):
    recurring = RecurringTransaction.objects.filter(
        user=request.user
    ).select_related('category').order_by('next_date')
    return render(request, 'recurring/list.html', {'recurring': recurring})


@login_required
def recurring_create(request):
    if request.method == 'POST':
        form = RecurringTransactionForm(request.user, request.POST)
        if form.is_valid():
            r = form.save(commit=False)
            r.user = request.user
            r.save()
            messages.success(request, 'Recurring transaction created!')
            return redirect('recurring-list')
    else:
        form = RecurringTransactionForm(request.user)
    return render(request, 'recurring/form.html', {'form': form, 'action': 'Create'})


@login_required
def recurring_update(request, pk):
    recurring = get_object_or_404(RecurringTransaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RecurringTransactionForm(request.user, request.POST, instance=recurring)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recurring transaction updated!')
            return redirect('recurring-list')
    else:
        form = RecurringTransactionForm(request.user, instance=recurring)
    return render(request, 'recurring/form.html', {'form': form, 'action': 'Update'})


@login_required
def recurring_delete(request, pk):
    recurring = get_object_or_404(RecurringTransaction, pk=pk, user=request.user)
    if request.method == 'POST':
        recurring.delete()
        messages.success(request, 'Recurring transaction deleted.')
        return redirect('recurring-list')
    return render(request, 'recurring/confirm_delete.html', {'object': recurring})