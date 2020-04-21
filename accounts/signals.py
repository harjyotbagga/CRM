from django.db.models import post_save
from django.contrib.auth.models import User, Group
from .models import Customer

def customer_profile(sender, instance, create, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        user.groups.add(group)
        Customer.objects.create(user=user, name=user.username)

post_save.connect(customer_profile, sender=User)
