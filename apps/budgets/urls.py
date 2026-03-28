from django.urls import path
from . import views

urlpatterns = [
    path('', views.budget_list, name='budget-list'),
    path('create/', views.budget_create, name='budget-create'),
    path('<int:pk>/edit/', views.budget_update, name='budget-update'),
    path('<int:pk>/delete/', views.budget_delete, name='budget-delete'),
]
