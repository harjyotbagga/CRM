from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import Customer, Order, Product, Tag
from .forms import OrderForm, CustomerForm
# Create your views here.

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

def products(request):
    product_count = Product.objects.count()
    products = Product.objects.all()
    context = {
        "product_count": product_count,
        "products": products
    }
    return render(request, 'products.html', context=context)

def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    customer_order_set = customer.customer_orders.all()
    customer_order_set_count = customer.customer_orders.count()
    context = {
        'customer': customer,
        'customer_order_set': customer_order_set,
        'customer_order_set_count': customer_order_set_count
    }
    return render(request, 'customer.html', context=context)

def create_order(request):
    if request.method == 'GET':
        form = OrderForm()
        context={'form': form}
        return render(request, 'order_form.html', context=context)
    elif request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

def create_customer_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=pk)
    if request.method == 'GET':
        formset = OrderFormSet(instance=customer)
        context={'customer': customer, 'formset': formset}
        return render(request, 'customer_order_form.html', context=context)
    elif request.method == 'POST':
        # FIXME: Yet to sort out the management error
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

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
        return redirect('/')

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
        return redirect('/')

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
        return redirect('/')

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
        return redirect('/')