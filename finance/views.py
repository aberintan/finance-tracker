# Imports for views to render HTML templates (Django)
from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, RecurringInvoice, Budget
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Imports for API endpoints (React)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import TransactionSerializer, RecurringInvoiceSerializer, BudgetSerializer
from rest_framework.authentication import TokenAuthentication

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Views to render HTML templates (Django)
@login_required  # Ensure the user is logged in
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)  # Filter transactions for the logged-in user
    return render(request, 'transaction_list.html', {'transactions': transactions})

@login_required
def transaction_add(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        date = request.POST['date']
        category = request.POST['category']
        payment_method = request.POST['payment_method']
        notes = request.POST.get('notes', '')

        transaction = Transaction(
            user=request.user,
            amount=amount,
            date=date,
            category=category,
            payment_method=payment_method,
            notes=notes
        )
        transaction.save()
        return redirect('transaction_list')  # Redirect to the transaction list after saving

    return render(request, 'transaction_add.html')  # Render a form for adding a transaction

@login_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    return render(request, 'transaction_detail.html', {'transaction': transaction})

@login_required
def recurring_invoice_list(request):
    invoices = RecurringInvoice.objects.filter(user=request.user)
    return render(request, 'recurring_invoice_list.html', {'invoices': invoices})

@login_required
def recurring_invoice_add(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        due_date = request.POST['due_date']
        category = request.POST['category']
        payment_method = request.POST['payment_method']

        invoice = RecurringInvoice(
            user=request.user,
            amount=amount,
            due_date=due_date,
            category=category,
            payment_method=payment_method
        )
        invoice.save()
        return redirect('recurring_invoice_list')

    return render(request, 'recurring_invoice_add.html')

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    return render(request, 'budget_list.html', {'budgets': budgets})

@login_required
def budget_add(request):
    if request.method == 'POST':
        category = request.POST['category']
        limit = request.POST['limit']

        budget = Budget(
            user=request.user,
            category=category,
            limit=limit
        )
        budget.save()
        return redirect('budget_list')

    return render(request, 'budget_add.html')

# API endpoints using DRF viewsets (React)
class TransactionViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RecurringInvoiceViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = RecurringInvoiceSerializer

    def get_queryset(self):
        return RecurringInvoice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })