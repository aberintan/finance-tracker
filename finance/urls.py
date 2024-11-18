from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.transaction_add, name='transaction_add'),
    path('transactions/<int:pk>/', views.transaction_detail, name='transaction_detail'),
    
    path('recurring-invoices/', views.recurring_invoice_list, name='recurring_invoice_list'),
    path('recurring-invoices/add/', views.recurring_invoice_add, name='recurring_invoice_add'),

    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/add/', views.budget_add, name='budget_add'),
]