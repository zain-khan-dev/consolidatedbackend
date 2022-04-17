from django.http import HttpResponse
from django.shortcuts import render

from rssfeeder.serializers import RSSSerializer, HeaderSerializer, UserSerializer
from .utils.Constants import NDTV, QUINT, HACKERNOON
from .utils.utility import getRSSData
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import exception_handler, APIView
from rest_framework.permissions import IsAuthenticated
# Create your views here.


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response



class index(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):
        print(request)
        data = getRSSData(NDTV)
        header = data["header"]
        print(header)
        serializer = RSSSerializer(data=data)
        if(serializer.is_valid()):
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return HttpResponse("Working")


    

class SignupView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


    