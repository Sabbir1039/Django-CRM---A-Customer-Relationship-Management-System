from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CustomerForm
from django.forms import inlineformset_factory

# Create your views here.
def dashboard(request):
    orders = Order.objects.all()
    recent_orders = orders.order_by('-id')[:5]
    total_order = orders.count()
    customers = Customer.objects.all()
    recent_customers = customers.order_by('-id')[:5]
    total_customer = customers.count()
    status = Order.objects.filter(status="Pending")
    pending_order = status.count()
    
    context = {
        'orders': recent_orders,
        'total_order': total_order,
        'customers': recent_customers,
        'total_customer': total_customer,
        'pending_order': pending_order,
    }
    return render(request, 'mainApp/dashboard.html', context)

def customers(request):
    customers = Customer.objects.all()
    total_customer = customers.count()
    context = {
        'customers': customers,
        'total_customer': total_customer,
    }
    return render(request, 'mainApp/customers.html', context)

def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_order = orders.count()
    context = {
        'customer': customer,
        'orders': orders,
        'total_order': total_order,
    }
    return render(request, 'mainApp/customer_profile.html', context)
def products(request):
    products = Product.objects.all()
    total_product = products.count()
    context = {
        'products': products,
        'total_product': total_product,
    }
    return render(request, 'mainApp/products.html', context)

def orders(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    pending = orders.filter(status="Pending").count()
    delivered = orders.filter(status="Delivered").count()
    out_for_delevery = orders.filter(status="Out for delevery").count()
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'pending': pending,
        'delivered': delivered,
        'out_for_delevery': out_for_delevery,    
    }
    return render(request, 'mainApp/orders.html', context)

def order_form(request):
    form = OrderForm
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    
    context = {
        'form': form,
        'title': 'Place New Order',
    }
    return render(request, 'mainApp/order_form.html', context)

def customer_multiple_order_form(request, pk):
    Orderformset = inlineformset_factory(Customer, Order, fields=('product', 'quantity', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    formset = Orderformset(queryset=Order.objects.none(), instance=customer)
    if request.method == "POST":
        formset = Orderformset(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('customer', pk=pk)
    context = {
        'formset': formset,
        'customer': customer,
    }
    return render(request, 'mainApp/customer_order_form.html', context)

def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
        return redirect('orders')
    context = {
        'form': form,
        'title': 'Update Order',
    }
    return render(request, 'mainApp/order_form.html', context)

def delete_order(request, pk):
    item = Order.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('orders')
    context = {
        'item': item,
    }
    return render(request, 'mainApp/delete.html', context)

def add_customer(request):
    form = CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid:
            form.save()
        return redirect('customers')
    context = {
        'form': form,
        'title': 'Add Customer',
    }
    return render(request, 'mainApp/customer_form.html', context)

def update_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
        return redirect('customers')
    context = {
        'form': form,
        'title': 'Update Customer',
    }
    return render(request, 'mainApp/customer_form.html', context)

def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('customers')
    context = {
        'customer': customer,
    }
    return render(request, 'mainApp/delete_customer.html', context)