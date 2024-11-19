from django.shortcuts import render, redirect, get_object_or_404
from .models import Transaction, RecurringInvoice, Budget
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

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
