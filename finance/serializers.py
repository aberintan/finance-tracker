from rest_framework import serializers
from .models import Transaction, RecurringInvoice, Budget

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'amount', 'date', 'category', 'payment_method', 'notes']

class RecurringInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringInvoice
        fields = ['id', 'user', 'amount', 'due_date', 'category', 'payment_method']

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'user', 'category', 'limit']
