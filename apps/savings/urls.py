from django.urls import path
from . import views

urlpatterns = [
    path('', views.savings_list, name='savings-list'),
    path('create/', views.savings_create, name='savings-create'),
    path('<int:pk>/edit/', views.savings_update, name='savings-update'),
    path('<int:pk>/deposit/', views.savings_deposit, name='savings-deposit'),
    path('<int:pk>/delete/', views.savings_delete, name='savings-delete'),
]
