from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .models import *
from .forms import *
from .filters import *
from .decorators import *
# Create your views here.

@unauthenticated_users
def loginPage(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username/Password is incorrect.')
            return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_users
def register(request):
    if request.method == 'GET':
        form = CreateUserForm()
        context = {'form': form}
        return render(request, 'register.html', context=context)
    elif request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'User account was created for '+ str(username))
            return redirect('login')
        else:
            return render(request, 'register.html', context={'form': form})

@login_required(login_url='login')
@authorized_users(allowed_roles = ['customer'])
def userPage(request):
    orders = request.user.customer.customer_orders.all()
    order_count = request.user.customer.customer_orders.count()
    delivered_order_count = request.user.customer.customer_orders.filter(status='Delivered').count()
    pending_order_count = request.user.customer.customer_orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'order_count': order_count,
        'delivered_order_count': delivered_order_count,
        'pending_order_count': pending_order_count
    }
    return render(request, 'user.html', context=context)


@login_required(login_url='login')
@authorized_users(allowed_roles = ['admin', 'customer'])
@admin_only
def home(request):
    customer_count = Customer.objects.count()
    customers = Customer.objects.all()
    orders = Order.objects.all()
    order_count = Order.objects.count()
    delivered_order_count = Order.objects.filter(status='Delivered').count()
    pending_order_count = Order.objects.filter(status='Pending').count()
    context = {
        'customer_count': customer_count,
        'customers': customers,
        'orders': orders,
        'order_count': order_count,
        'delivered_order_count': delivered_order_count,
        'pending_order_count': pending_order_count
    }
    return render(request, 'dashboard.html', context=context)

@login_required(login_url='login')
@authorized_users(allowed_roles = ['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'GET':
        context = {'form':form}
        return render(request, 'account_settings.html', context)
    elif request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
        else:
            print(form.errors)
        context = {'form':form}
        return render(request, 'account_settings.html', context)

@login_required(login_url='login')
@authorized_users(allowed_roles = ['admin'])
def products(request):
    product_count = Product.objects.count()
    products = Product.objects.all()
    context = {
        "product_count": product_count,
        "products": products
    }
    return render(request, 'products.html', context=context)

@login_required(login_url='login')
@authorized_users(allowed_roles = ['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    customer_order_set = customer.customer_orders.all()
    customer_order_set_count = customer.customer_orders.count()
    CustomerOrderFilter = OrderFilter(request.GET, queryset=customer_order_set)
    customer_order_set = CustomerOrderFilter.qs
    context = {
        'customer': customer,
        'customer_order_set': customer_order_set,
        'customer_order_set_count': customer_order_set_count,
        'CustomerOrderFilter': CustomerOrderFilter
    }
    return render(request, 'customer.html', context=context)

@login_required(login_url='login')
@authorized_users(allowed_roles = ['admin'])
def create_order(request):
    if request.method == 'GET':
        form = OrderForm()
        context={'form': form}
        return render(request, 'order_form.html', context=context)
    elif request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

@login_required(login_url='login')
@authorized_users(allowed_roles = ['admin', 'customer'])
# TODO: Add a func, to allow that customer only to create an order
def create_customer_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=pk)
    if request.method == 'GET':
        formset = OrderFormSet(instance=customer)
        context={
            'customer': customer, 
            'formset': formset}
        return render(request, 'customer_order_form.html', context=context)
    elif request.method == 'POST':
        # FIXME: Yet to sort out the management error
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')

@login_required(login_url='login')
@authorized_users(allowed_roles=['admin', 'customer'])
# TODO: Add a func, to allow that customer only to update an order
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'GET':
        form = OrderForm(instance=order)
        context = {'form': form}
        return render(request, 'order_form.html', context=context)
    elif request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
        return redirect('home')

@login_required(login_url='login')
@authorized_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'GET':
        context = {
            'order_product': order.product,
            'order_date_created': order.date_created
        }
        return render(request, 'delete_order.html', context=context)
    if request.method == 'POST':
        if request.POST['Submit'] == 'Delete':
            order.delete()
        return redirect('home')

@login_required(login_url='login')
@authorized_users(allowed_roles=['admin'])
def update_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'GET':
        form = CustomerForm(instance=customer)
        context = {'form': form}
        return render(request, 'customer_form.html', context=context)
    elif request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
        return redirect('home')

@login_required(login_url='login')
@authorized_users(allowed_roles=['admin'])
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'GET':
        context = {
            'customer_name': customer.name
        }
        return render(request, 'delete_customer.html', context=context)
    if request.method == 'POST':
        if request.POST['Submit'] == 'Delete':
            customer.delete()
        return redirect('home')
