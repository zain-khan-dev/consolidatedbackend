from wsgiref import validate
from rest_framework import serializers
from .models import Customer, Seller, Product, Order
from django.contrib.auth.models import User




class UserSeralizer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [ 'username', 'password']





class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields=['id','name','description']


class OrderCustomerSerializer(serializers.ModelSerializer):
    

    product_id =  ProductDetailSerializer()

    class Meta:
        model = Order
        fields = ['id','product_id', 'order_ts', 'status']


class CustomerDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ['id','name']

class OrderProductSerializer(serializers.ModelSerializer):

    customer_id = CustomerDetailSerializer()

    class Meta:
        model = Order
        fields = ['id','customer_id', 'order_ts', 'status']

    

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class CustomerSeralizer(serializers.ModelSerializer):

    user = UserSeralizer()

    orders = OrderCustomerSerializer(many=True, read_only=True)

    # orders = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = '__all__'



    def create(self, validated_data):
        print(validated_data)
        username = validated_data["user"]["username"]
        password = validated_data["user"]["password"]
        validated_data.pop('user')
        # return Customer.objects.create(**validated_data)
        user = User.objects.create_user(username=username, password=password)
        return Customer.objects.create(user=user, **validated_data)


    
        



class SerllerSerializer(serializers.ModelSerializer):

    user = UserSeralizer()



    class Meta:
        model = Seller
        fields = '__all__'


    def create(self, validated_data):
        print(validated_data)
        username = validated_data["user"]["username"]
        password = validated_data["user"]["password"]
        validated_data.pop('user')
        # return Customer.objects.create(**validated_data)
        user = User.objects.create_user(username=username, password=password)
        return Seller.objects.create(user=user, **validated_data)




class ProductSeralizer(serializers.ModelSerializer):

    orders = OrderProductSerializer(many=True, read_only=True)


    class Meta:
        model = Product
        fields = '__all__'



