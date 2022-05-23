import json
from unicodedata import category
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render
from ecommerce import serialzers
from rest_framework.viewsets import ModelViewSet

from ecommerce.serialzers import CustomerSeralizer, ProductSeralizer, SellerSerializer
from .models import ProfileUser, Order, Product, ProductImage
from rest_framework.response import Response
from rest_framework.generics import  RetrieveDestroyAPIView, CreateAPIView
from rest_framework import permissions
from .serialzers import CartSerializer, ProductImageSerializer, ProductViewSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin
from rest_framework.status import HTTP_404_NOT_FOUND
from .models import Cart
from .serialzers import AddCartSerializer, ViewOrderSerializer, PlaceOrderSerializer


# Create your views here.



class CustomerViewSet(ModelViewSet):
    queryset = ProfileUser.objects.filter(type="C")
    serializer_class = CustomerSeralizer


class SellerViewSet(ModelViewSet):
    queryset = ProfileUser.objects.filter(type="S")
    serializer_class = SellerSerializer



class ProductViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()



    def get_serializer_class(self, *args, **kwargs):
        if(self.action == "retrieve" or self.action == "list"):
            return ProductSeralizer
        else:
            return  ProductViewSerializer


#   name = models.CharField(max_length=200, null=False)


    def create(self,request, *args, **kwargs):
        user = self.request.user
        print(self.request.FILES)

        # name = self.request.POST.get("name")
        # description = self.request.POST.get("description")
        # description = self.request.POST.get("price")
        seller = ProfileUser.objects.filter(user=user, type="S").first()
        name = self.request.POST.get("name")
        description = self.request.POST.get("description")
        price = self.request.POST.get("price")
        stock = self.request.POST.get("stock")
        category = self.request.POST.get("category")
        product = Product(name=name, description=description, price=price, stock=stock, category=category, seller = seller)
        product.save()
        productSerializer = ProductViewSerializer(instance=product)
        
        # serializer.save(seller_id=seller.id)
        for file in self.request.FILES.values():
            print(file)
            productImage = ProductImage(image=file, product_id=product)
            productImage.save()
            productSerializer = ProductImageSerializer(productImage)

        return Response(productSerializer.data)


class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    # serializer_class = ViewOrderSerializer

    permission_class = [permissions.IsAuthenticated]



    def get_serializer_class(self, *args, **kwargs):
        if(self.action == "retrieve" or self.action == "list"):
            return ViewOrderSerializer
        else:
            return PlaceOrderSerializer
        

    def list(self, request):
        user = request.user
        profile = ProfileUser.objects.filter(user = user).prefetch_related("orders").first()
        if(profile.type == "S"): # if a seller getting order list
            products = Product.objects.filter(seller=profile).prefetch_related("orders").all()
            orders = list(map(lambda product:product.orders.all(), products))
            serializedOrders = ViewOrderSerializer(*orders, many=True)
            print(serializedOrders.data)
        else: # if a customer getting order list
            print(profile.orders)
            serializedOrders = ViewOrderSerializer(profile.orders, many=True)
        return Response(serializedOrders.data)


    
    def perform_create(self, serializer):
        user = self.request.user
        customer = ProfileUser.objects.filter(user=user, type='C').first()
        print(customer)
        serializer.save(customer_id=customer)


class AddToCardView(CreateAPIView):
    serializer_class = AddCartSerializer

    def perform_create(self, serializer):
        user = self.request.user
        customer = ProfileUser.objects.filter(user=user, type='C').first()
        serializer.save(customer_id=customer)





class UserCartView(APIView):

    permission_class = [permissions.IsAuthenticated]


    def get(self, request):
        user = request.user
        customer = ProfileUser.objects.filter(user=user, type="C").first()
        print(customer)
        print(customer.id)
        cartItems = CartSerializer(customer.cart.select_related('product_id').all(), many=True)
        return Response(cartItems.data)





class CustomerOrderView(APIView):



    def get(self, request, *args, **kwargs):
        customer_id = kwargs.get("cid", None)
        if(customer_id == None):
            return Response(status=HTTP_404_NOT_FOUND)
        else:
            customer_orders = Order.objects.filter(customer_id=customer_id)
            serializer = ViewOrderSerializer(customer_orders, many=True)
            return Response(serializer.data)





class CategoryView(APIView):
    def get(self, request, *args, **kwargs):
        categoryType = kwargs["type"]
        products = Product.objects.filter(category=categoryType)
        serializer = ProductViewSerializer(products, many=True)
        return Response(serializer.data)


class UploadImage(ListCreateAPIView):
    
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()