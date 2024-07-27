from rest_framework.decorators import  api_view,action
from rest_framework.response   import Response
from rest_framework import status
from django.contrib.auth.models import  User
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import ModelViewSet
from . serializers  import UserSerializer
from django.shortcuts import get_object_or_404
from django.db import transaction

class UserViewset(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('-id')
    @transaction.atomic
    def create(self,request):
        request_data = request.data
        serializer = UserSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request_data['username'])
            user.set_password(request_data['password'])
            user.save()
            token = Token.objects.create(user=user)
            
            return Response({"token":token.key,"user":serializer.data})
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['POST'],detail=False,url_name='login',url_path='login')
    def login(self,request):
        user = get_object_or_404(User,username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response("invalid login credentials",status=status.HTTP_400_BAD_REQUEST)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)
        return Response({"token":token.key,"user":serializer.data})
            
    @action(methods=['GET'],detail=False,url_name='token',url_path='token')
    def test_token(self,request):
        import requests
        url = 'http://127.0.0.1:8080/hospital/departments/'
        headers = {'Authorization': 'Token 391d70182a7eeb6bdba7a6b392e8b9f29bc7ba5c'}
        response = requests.get(url, headers=headers)
        print(response.json())

        return Response("heee")