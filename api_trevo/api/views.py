from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import UserModel
from .serializer import UserModelSerializer


# Create your views here.

@api_view(['GET'])
def get_routes(request):
    routes = [
        '',
        'tickets/',
        'tickets/<id>',
    ]
    return Response(routes, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_users(request):
    users = UserModel.objects.all()
    serializer = UserModelSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user(request, user_id):
    user = UserModel.objects.get(id=user_id)
    serializer = UserModelSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_user(request, user_id):
    user = UserModel.objects.get(id=user_id)
    data = request.data

    seralizer = UserModelSerializer(instance=user, data=data)

    if seralizer.is_valid():
        seralizer.save()

    return Response(seralizer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_user(request, user_id):
    user = UserModel.objects.get(id=user_id)
    user.delete()
    return Response('', status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def create_user(request):
    data = request.data
    new_user = UserModel.objects.create(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        password=data['password'],
    )
    serializer = UserModelSerializer(new_user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
