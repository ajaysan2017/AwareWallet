from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transactions/', views.transaction_list, name='transaction-list'),
    path('transactions/add/', views.transaction_create, name='transaction-create'),
    path('transactions/<int:pk>/edit/', views.transaction_update, name='transaction-update'),
    path('transactions/<int:pk>/delete/', views.transaction_delete, name='transaction-delete'),
]
