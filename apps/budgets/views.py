from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Budget
from .forms import BudgetForm


@login_required
def budget_list(request):
    today = timezone.now().date()
    budgets = Budget.objects.filter(
        user=request.user,
        month__year=today.year,
        month__month=today.month
    ).select_related('category')
    return render(request, 'budgets/list.html', {'budgets': budgets, 'today': today})


@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.user, request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget created!')
            return redirect('budget-list')
        # form.is_valid() failed — fall through to re-render with errors
    else:
        form = BudgetForm(request.user)
    return render(request, 'budgets/form.html', {'form': form, 'action': 'Create'})


@login_required
def budget_update(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.user, request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated!')
            return redirect('budget-list')
    else:
        form = BudgetForm(request.user, instance=budget)
    return render(request, 'budgets/form.html', {'form': form, 'action': 'Update'})


@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted.')
        return redirect('budget-list')
    return render(request, 'budgets/confirm_delete.html', {'object': budget})