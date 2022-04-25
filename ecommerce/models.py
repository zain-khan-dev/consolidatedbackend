from django.db import models
from django.contrib.auth.models import User
from .utils.Constants import OrderStatus
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, related_name='users')
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=2000)
    phone_number = models.CharField(max_length=20)





class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    address = models.CharField(max_length=2000, null=False)
    phone_number = models.CharField(max_length=20)



class Product(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=2000, null=False)
    stars = models.IntegerField(default=5,validators=[MinValueValidator(1), MaxValueValidator(5)])
    seller = models.ForeignKey(Seller,on_delete=models.CASCADE,related_name='seller')



class Order(models.Model):
    customer_id = models.ForeignKey(Customer,on_delete=models.CASCADE, related_name="orders")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    order_ts = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=OrderStatus, max_length=40)

