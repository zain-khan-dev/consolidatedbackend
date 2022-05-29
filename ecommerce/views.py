import json
from unicodedata import category

from django.http import HttpResponse, JsonResponse, QueryDict
from django.shortcuts import render
from ecommerce import serialzers
from rest_framework.viewsets import ModelViewSet

from ecommerce.serialzers import CustomerSeralizer, ProductSerializer, SellerSerializer
from .models import ProductFeature, ProductSpecification, ProfileUser, Order, Product, ProductImage
from rest_framework.response import Response
from rest_framework.generics import  RetrieveDestroyAPIView, CreateAPIView
from rest_framework import permissions
from .serialzers import CartSerializer, CommentSerializer, ProductFeatureSerializer, ProductImageSerializer, ProductSpecsSerializer, ProductViewSeralizer
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import DestroyModelMixin, RetrieveModelMixin
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.generics import GenericAPIView, ListAPIView
from .models import Cart, Comment
from .serialzers import AddCartSerializer, ViewOrderSerializer, PlaceOrderSerializer
from rest_framework.decorators import api_view


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
            return ProductViewSeralizer
        else:
            return  ProductSerializer


#   name = models.CharField(max_length=200, null=False) 


    def create(self,request, *args, **kwargs):
        user = self.request.user

        # name = self.request.POST.get("name")
        # description = self.request.POST.get("description")
        # description = self.request.POST.get("price")
        seller = ProfileUser.objects.filter(user=user, type="S").first()
        name = self.request.POST.get("name")
        description = self.request.POST.get("description")
        price = self.request.POST.get("price")
        stock = self.request.POST.get("stock")
        category = self.request.POST.get("category")
        discount = self.request.POST.get("discount")
        width = self.request.POST.get("width")
        height = self.request.POST.get("height")
        metric = self.request.POST.get("metric")
        model_no = self.request.POST.get("model")
        release_date = self.request.POST.get("release_date")
        manufacturer_name = self.request.POST.get("manufacturer_name")
        expiry_date = self.request.POST.get("expiry_date")
        country_of_origin = self.request.POST.get("country_of_origin")

        if(discount == ""):
            discount = 0
        
        product = Product(name=name, description=description, price=price, stock=stock, category=category, seller = seller, discount=discount)
        product.save()
        productSerializer = ProductSerializer(instance=product)
        
        # Add features 
        features = [ProductFeature(product_id=product , description=value) for key,value in self.request.POST.items() if key.split('.')[0] == 'features']

        ProductFeature.objects.bulk_create(features)


        # create product images for the saved product reference
        productImages = [ProductImage(src=file, product_id=product) for file in self.request.FILES.values()]
        ProductImage.objects.bulk_create(productImages)


        # create product specification for the saved product reference

        specs = ProductSpecification(product_id = product, width=width, height=height,measure_type=metric,
        model_no=model_no,release_date=release_date,manufacturer_name=manufacturer_name, country_of_origin=country_of_origin, expiry_date=expiry_date)

        specs.save()

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



class CommentView(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all() 



class CategoryView(APIView):
    def get(self, request, *args, **kwargs):
        categoryType = kwargs["type"]
        products = Product.objects.filter(category=categoryType)
        serializer = ProductViewSeralizer(products, many=True)
        return Response(serializer.data)


class UploadImage(ListCreateAPIView):
    
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()





class ProductSpecs(ListCreateAPIView):

    serializer_class = ProductSpecsSerializer
    queryset = ProductSpecification.objects.all()


class ProductFeatureView(ListCreateAPIView):

    serializer_class = ProductFeatureSerializer
    queryset = ProductFeature.objects.all()


@api_view(["GET"])
def getSearchResult(request, *args, **kwargs):
    query = kwargs["query"]
    products = Product.objects.filter(name__contains=query)
    return Response(ProductViewSeralizer(products, many=True).data)
