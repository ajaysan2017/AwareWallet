"""
Category views for AwareWallet.
 
Handles category listing, creation, updating and deletion.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category
from .forms import CategoryForm


@login_required
def category_list(request):
    income_cats = Category.objects.filter(user=request.user, type='income') | \
                  Category.objects.filter(is_default=True, type='income')
    expense_cats = Category.objects.filter(user=request.user, type='expense') | \
                   Category.objects.filter(is_default=True, type='expense')
    return render(request, 'categories/list.html', {
        'income_categories': income_cats.distinct(),
        'expense_categories': expense_cats.distinct(),
    })


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.user, request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, f'Category "{category.name}" created!')
            return redirect('category-list')
    else:
        form = CategoryForm(request.user)
    return render(request, 'categories/form.html', {'form': form, 'action': 'Create'})


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.user, request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category "{category.name}" updated!')
            return redirect('category-list')
    else:
        form = CategoryForm(request.user, instance=category)
    return render(request, 'categories/form.html', {'form': form, 'action': 'Update'})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'Category "{name}" deleted.')
        return redirect('category-list')
    return render(request, 'categories/confirm_delete.html', {'object': category})
