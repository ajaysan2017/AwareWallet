from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SavingsGoal
from .forms import SavingsGoalForm, SavingsDepositForm


@login_required
def savings_list(request):
    goals = SavingsGoal.objects.filter(user=request.user)
    active = goals.filter(is_completed=False)
    completed = goals.filter(is_completed=True)
    return render(request, 'savings/list.html', {
        'active_goals': active,
        'completed_goals': completed,
    })


@login_required
def savings_create(request):
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, f'Savings goal "{goal.goal_name}" created!')
            return redirect('savings-list')
    else:
        form = SavingsGoalForm()
    return render(request, 'savings/form.html', {'form': form, 'action': 'Create'})


@login_required
def savings_update(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SavingsGoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Savings goal updated!')
            return redirect('savings-list')
    else:
        form = SavingsGoalForm(instance=goal)
    return render(request, 'savings/form.html', {'form': form, 'action': 'Update'})


@login_required
def savings_deposit(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SavingsDepositForm(request.POST)
        if form.is_valid():
            goal.current_amount += form.cleaned_data['amount']
            if goal.current_amount >= goal.target_amount:
                goal.is_completed = True
                messages.success(request, f'🎉 Goal "{goal.goal_name}" completed!')
            else:
                messages.success(request, f'Added to "{goal.goal_name}"! {goal.percentage_complete}% complete.')
            goal.save()
            return redirect('savings-list')
    else:
        form = SavingsDepositForm()
    return render(request, 'savings/deposit.html', {'form': form, 'goal': goal})


@login_required
def savings_delete(request, pk):
    goal = get_object_or_404(SavingsGoal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Savings goal deleted.')
        return redirect('savings-list')
    return render(request, 'savings/confirm_delete.html', {'object': goal})