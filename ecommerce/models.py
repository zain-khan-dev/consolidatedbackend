from django.db import models
from django.contrib.auth.models import User
from .utils.Constants import OrderStatus, PRODUCT_CATEGORIES, MEASURE_TYPES
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, related_name='users')
    name = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=2000)
    phone_number = models.CharField(max_length=20)
    type = models.CharField(choices=[("S","Seller"),( "C","Customer")], max_length=10)



class Product(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=2000, null=False)
    stars = models.IntegerField(default=5,validators=[MinValueValidator(1), MaxValueValidator(5)])
    seller = models.ForeignKey(ProfileUser,on_delete=models.CASCADE, related_name='seller')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    category = models.CharField(choices=PRODUCT_CATEGORIES, max_length=50)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(99)]) # discount can vary only beteween 0 and 99


class ProductImage(models.Model):
    image = models.ImageField()
    product_id = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name="images")



class ProductSpecification(models.Model):
    width = models.DecimalField(max_digits=8, decimal_places=2)
    height = models.DecimalField(max_digits=8, decimal_places=2)
    measure_type = models.CharField(max_length=100, choices=MEASURE_TYPES)
    model_no = models.CharField(max_length=50)
    release_date = models.DateField(default=datetime.today)
    manufacturer_name = models.CharField(max_length=100)
    product_id = models.ForeignKey(to=Product, on_delete=models.CASCADE, related_name="specs")


class Order(models.Model):
    customer_id = models.ForeignKey(ProfileUser,on_delete=models.CASCADE, related_name="orders")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    order_ts = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=OrderStatus, max_length=40)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)



class Comment(models.Model):
    comment_by = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.CharField(max_length=2000)
    comment_to = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')


class Cart(models.Model):
    customer_id = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, related_name="cart")
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cartitem")
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)