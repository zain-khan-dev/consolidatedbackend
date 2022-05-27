from wsgiref import validate
from rest_framework import serializers
from .models import Cart, ProductFeature, ProductImage, ProductSpecification, ProfileUser, Product, Order, Comment
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
        model = ProfileUser
        fields = ['id','name']




class OrderProductSerializer(serializers.ModelSerializer):

    customer_id = CustomerDetailSerializer()

    class Meta:
        model = Order
        fields = ['id','customer_id', 'order_ts', 'status']



class AddCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = ['product_id', 'quantity']


class CartSerializer(serializers.ModelSerializer):

    product_id = ProductDetailSerializer()

    class Meta:
        model = Cart
        fields = ['product_id', 'quantity', 'price']
    

class ViewOrderSerializer(serializers.ModelSerializer):


    product_id = ProductDetailSerializer()

    class Meta:
        model = Order
        fields = ['product_id', 'status', 'price', 'order_ts', 'quantity']



class CartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'


class UserCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileUser
        fields = ['cart']



class CartUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ["product_id"]


class CustomerSeralizer(serializers.ModelSerializer):

    user = UserSeralizer()

    orders = OrderCustomerSerializer(many=True, read_only=True)

    cart = CartUserSerializer(many=True, read_only=True)

    # orders = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = ProfileUser
        fields = ['user', 'name','address','phone_number', 'orders', 'cart']



    def create(self, validated_data):
        print(validated_data)
        username = validated_data["user"]["username"]
        password = validated_data["user"]["password"]
        validated_data.pop('user')
        # return Customer.objects.create(**validated_data)
        user = User.objects.create_user(username=username, password=password)
        return ProfileUser.objects.create(user=user,type='C', **validated_data)


    
class PlaceOrderSerializer(serializers.ModelSerializer):

    customer_id = CustomerSeralizer(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = '__all__'





class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = '__all__'
    


class SellerSerializer(serializers.ModelSerializer):

    user = UserSeralizer()



    class Meta:
        model = ProfileUser
        fields = ['user', 'name','address','phone_number']


    def create(self, validated_data):
        print(validated_data)
        username = validated_data["user"]["username"]
        password = validated_data["user"]["password"]
        validated_data.pop('user')
        # return Customer.objects.create(**validated_data)
        user = User.objects.create_user(username=username, password=password)
        return ProfileUser.objects.create(user=user,type='S', **validated_data)



class ProductViewSerializer(serializers.ModelSerializer):

    seller = SellerSerializer(read_only=True)


    class Meta:
        model=Product
        fields = "__all__"


class ProductSpecsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductSpecification
        fields = '__all__'




class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'



class ProductFeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductFeature
        fields = '__all__'

class ProductSeralizer(serializers.ModelSerializer):

    # orders = OrderProductSerializer(many=True, read_only=True)

    # seller = serializers.CharField(source='seller.name', read_osnly=True)
    # seller = SerllerSerializer(read_only=True)

    images = ProductImageSerializer(many=True)
    
    specs = ProductSpecsSerializer()

    features = ProductFeatureSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'



