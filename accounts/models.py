from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.
def upload_photo_and_rename(instance, filename):
    upload_to = 'users/'+instance.name
    ext = filename.split('.')[-1]
    filename = 'profile_pic'+'.'+str(ext)
    return os.path.join(upload_to, filename)

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=False)
    phone = models.BigIntegerField(null=False)
    email = models.EmailField(null=True)
    profile_pic = models.ImageField(default='default_profile_pic.png', null=True, blank=True, upload_to=upload_photo_and_rename)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50, null=False)
    price = models.FloatField(null=False)
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor')
    )
    category = models.CharField(max_length=50, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='tag_set')

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for Delivery', "Out for Delivery"),
        ('Delivered', 'Delivered')
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL, related_name='customer_orders')
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name='product_orders')
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS, null=False, max_length=50)

    def __str__(self):
        return str(self.customer) + ' - ' + str(self.date_created)
