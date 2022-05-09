import json
from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render
from ecommerce import serialzers
from rest_framework.viewsets import ModelViewSet

from ecommerce.serialzers import CustomerSeralizer, OrderSerializer, ProductSeralizer, SerllerSerializer
from .models import ProfileUser, Order, Product
from rest_framework.response import Response
from rest_framework.generics import  RetrieveDestroyAPIView, CreateAPIView
from rest_framework import permissions
from .serialzers import CartSerializer, ProductViewSerializer
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin
from rest_framework.status import HTTP_404_NOT_FOUND
from .models import Cart
from .serialzers import UserCartSerializer, CartItemSerializer, AddCartSerializer


# Create your views here.



class CustomerViewSet(ModelViewSet):
    queryset = ProfileUser.objects.filter(type="C")
    serializer_class = CustomerSeralizer


    


class CustomerRemove(RetrieveDestroyAPIView):
    queryset = ProfileUser.objects.filter(type="C")
    serializer_class = CustomerSeralizer



class SellerViewSet(ModelViewSet):
    queryset = ProfileUser.objects.filter(type="S")
    serializer_class = SerllerSerializer



class ProductViewSet(ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSeralizer


    def get_serializer_class(self, *args, **kwargs):
        if(self.action == "retrieve" or self.action == "list"):
            return ProductViewSerializer
        else:
            return ProductSeralizer


    def create(self, request, *args, **kwargs):
        name = request.data["title"]
        description = request.data["description"]
        user = request.user
        seller = ProfileUser.objects.filter(type="S", user=user).first()
        data = {"name":name, "description":description, "seller":seller.id}
        product = ProductSeralizer(data=data)
        if(product.is_valid()):
            product.save()
        else:
            print(product.errors)
        return Response(product.data)
    

    # def retrieve(self, request, *args, **kwargs):
    #     print(request.data, args, kwargs)
    #     productID = kwargs["pk"]
    #     print(productID)
    #     product = Product.objects.filter(id=productID).first()
    #     return Response(ProductViewSerializer(product).data)


class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        status = request.data["status"]
        product_id = request.data["product_id"]
        user = request.user
        customer = ProfileUser.objects.filter(user=user,type="C").first()
        product = Product.objects.filter(id = product_id).first()
        order = Order.objects.create(customer_id=customer, product_id=product, status=status)
        print(order)
        order.save()
        return Response({"first":"second"}) #TODO: Need to return the created order


class AddToCardView(APIView):


    serializer_class = AddCartSerializer

    def post(self, request):
        user = request.user
        product = request.data

        print(product["product_id"])
        product = Product.objects.get(id=product["product_id"])
        customer = ProfileUser.objects.filter(user = user, type="C").first()
        cart = Cart.objects.create(customer_id=customer, product_id=product)
        return Response(CartSerializer(cart).data)





class UserCartView(APIView):

    permission_class = [permissions.IsAuthenticated]


    def get(self, request):
        user = request.user
        customer = ProfileUser.objects.filter(user=user, type="C").first()
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
            serializer = OrderSerializer(customer_orders, many=True)
            return Response(serializer.data)


