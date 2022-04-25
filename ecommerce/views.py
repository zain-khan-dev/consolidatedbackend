import json
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render
from ecommerce import serialzers
from rest_framework.viewsets import ModelViewSet

from ecommerce.serialzers import CustomerSeralizer, OrderSerializer, ProductSeralizer, SerllerSerializer
from .models import Customer, Order, Seller, Product
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
# Create your views here.


def index(request):
    print(request)
    return HttpResponse("Hey there sexy man")




class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSeralizer


class CustomerRemove(RetrieveDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSeralizer



class SellerViews(ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SerllerSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSeralizer


class OrderView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer