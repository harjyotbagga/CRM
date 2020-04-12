from django.shortcuts import render
from django.http import HttpResponse
from .models import Customer, Order, Product, Tag
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