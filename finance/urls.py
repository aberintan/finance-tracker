from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import CustomAuthToken

# API endpoints (React)
router = DefaultRouter()
router.register(r'api/transactions', views.TransactionViewSet, basename='api-transaction')
router.register(r'api/recurring-invoices', views.RecurringInvoiceViewSet, basename='api-recurring-invoice')
router.register(r'api/budgets', views.BudgetViewSet, basename='api-budget')

urlpatterns = [
    # HTML templates (Django)
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/add/', views.transaction_add, name='transaction_add'),
    path('transactions/<int:pk>/', views.transaction_detail, name='transaction_detail'),

    path('recurring-invoices/', views.recurring_invoice_list, name='recurring_invoice_list'),
    path('recurring-invoices/add/', views.recurring_invoice_add, name='recurring_invoice_add'),

    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/add/', views.budget_add, name='budget_add'),

    # Include the router URLs
    path('', include(router.urls)),

    # Include the authentication URLs
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
]