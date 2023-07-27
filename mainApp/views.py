from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CustomerForm, ProductForm, UserForm
from django.forms import inlineformset_factory
from .filters import ProductFilter, OrderFilter, CustomerFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.


@unauthenticated_user
def register(request):

    form = UserForm
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
            )

            messages.success(
                request, 'Account has been created for ' + username)
            return redirect('loginpage')
    context = {
        'userform': form,
    }
    return render(request, 'mainApp/register.html', context)


@unauthenticated_user
def loginpage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or Password is not correct')
    return render(request, 'mainApp/loginpage.html')


def logoutpage(request):
    logout(request)
    return redirect('loginpage')


@login_required(login_url='loginpage')
@admin_only
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


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['customer'])
def accont_setting(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            # return redirect('user_page')
    context = {
        'form': form,
    }
    return render(request, 'mainApp/account_setting.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['customer'])
def user_page(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    deliverd = orders.filter(status='Deliverd').count()
    out_for_delivery = orders.filter(status='Out for delevery').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'deliverd': deliverd,
        'pending': pending,
        'out_for_delevery': out_for_delivery,
    }
    return render(request, 'mainApp/user.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def customers(request):
    customers = Customer.objects.all()
    total_customer = customers.count()
    customer_filter = CustomerFilter(request.GET, queryset=customers)
    customers = customer_filter.qs
    context = {
        'customers': customers,
        'total_customer': total_customer,
        'customer_filter': customer_filter,
    }
    return render(request, 'mainApp/customers.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    product_filter = ProductFilter(request.GET, queryset=products)
    products = product_filter.qs
    total_product = products.count()
    context = {
        'products': products,
        'total_product': total_product,
        'product_filter': product_filter,
    }
    return render(request, 'mainApp/products.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def product_form(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    context = {
        'form': form,
        'title': 'Add Product',
    }
    return render(request, 'mainApp/product_form.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def update_product(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')
    context = {
        'form': form,
        'title': 'Update Product',
        'product': product,
    }
    return render(request, 'mainApp/product_form.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def delete_product(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        return redirect('products')
    context = {
        'product': product,
    }
    return render(request, 'mainApp/delete_product.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def orders(request):
    orders = Order.objects.all()
    total_orders = orders.count()
    pending = orders.filter(status="Pending").count()
    delivered = orders.filter(status="Delivered").count()
    out_for_delevery = orders.filter(status="Out for delevery").count()
    order_filter = OrderFilter(request.GET, queryset=orders)
    orders = order_filter.qs
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'pending': pending,
        'delivered': delivered,
        'out_for_delevery': out_for_delevery,
        'order_filter': order_filter,
    }
    return render(request, 'mainApp/orders.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def customer_multiple_order_form(request, pk):
    Orderformset = inlineformset_factory(
        Customer, Order, fields=('product', 'quantity', 'status'), extra=5)
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


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    item = Order.objects.get(id=pk)
    if request.method == "POST":
        item.delete()
        return redirect('orders')
    context = {
        'item': item,
    }
    return render(request, 'mainApp/delete.html', context)


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
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


@login_required(login_url='loginpage')
@allowed_users(allowed_roles=['admin'])
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('customers')
    context = {
        'customer': customer,
    }
    return render(request, 'mainApp/delete_customer.html', context)
