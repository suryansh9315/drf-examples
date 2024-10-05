from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .utils import get_tokens_for_user

from .models import Product
from .serializers import ProductSerializer, RegistrationSerializer

class LoginUser(APIView):
    def post(self, request):
        if 'username' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login(request, user)
            auth_data = get_tokens_for_user(request.user)
            return Response({'msg': 'Login Success', **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# class LogoutUser(APIView):
#     def post(self, request):
#         logout(request)
#         return Response({'msg': 'Successfully Logged out'}, status=status.HTTP_200_OK)

class RegisterUser(APIView):
    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddProduct(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"msg": "Missing fields"}, status=404)
        serializer.save()
        return Response(serializer.data)

class GetProducts(APIView):
    def get(self, request, format=None):
        instance = Product.objects.all()
        products = ProductSerializer(instance, many=True).data
        return Response(products)

class GetProduct(APIView):
    def get(self, request, id, format=None):
        instance = Product.objects.filter(id = id)
        product = ProductSerializer(instance, many=True).data
        return Response(product)
