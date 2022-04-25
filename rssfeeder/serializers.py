from rest_framework import serializers
from django.contrib.auth.models import User

# "title", "link", "description", "category", "image"
class HeaderSerializer(serializers.Serializer):
    title  = serializers.CharField(max_length=2000, allow_null=True)
    link = serializers.CharField(max_length=2000, allow_null=True)
    description  = serializers.CharField(max_length=2000, allow_null=True)
    category = serializers.CharField(max_length=2000, allow_null=True)
    image  = serializers.CharField(max_length=2000, allow_null=True, allow_blank=True)
    


# "link", "title", "description", "category", "pubDate", "comments"
class ItemSerializer(serializers.Serializer):
    title  = serializers.CharField(max_length=2000, allow_null = True)
    link = serializers.CharField(max_length=2000, allow_null=True)
    description  = serializers.CharField(max_length=5000, allow_null=True)
    category = serializers.CharField(max_length=2000, allow_null=True)
    pubDate  = serializers.CharField(max_length=2000, allow_null=True)
    comments  = serializers.CharField(max_length=2000, allow_null=True)

class RSSSerializer(serializers.Serializer):
    header = HeaderSerializer(allow_null=True)
    items = ItemSerializer(many=True)



class UserSerializer(serializers.ModelSerializer):


    def create(self, validated_data):
        print("here")
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


    class Meta:
        model = User
        fields = ["first_name","username", "last_name", "password"]