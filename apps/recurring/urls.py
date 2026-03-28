from django.urls import path
from . import views

urlpatterns = [
    path('', views.recurring_list, name='recurring-list'),
    path('create/', views.recurring_create, name='recurring-create'),
    path('<int:pk>/edit/', views.recurring_update, name='recurring-update'),
    path('<int:pk>/delete/', views.recurring_delete, name='recurring-delete'),
]
