from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomLoginView(TokenObtainPairView):
    @extend_schema(
        summary="Login qilish uchun.",
        description="Foydalanuvchini authenticatsiya qilish va  token berish uchun ishlatiladi.",
        tags=['Auth'],
        request={
            "username": "admin",
            "password": "admin"
        },
        responses={
            200: {
                    "access": "Acces Token",
                    "refresh": "Refresh Token"
                }
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class TodoView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        description="Jami todolarni olish uchun API",
        tags=['Tasks']
    )
    def get(self, request:Request):
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    

    @extend_schema(
        description="Todo yaratish uchun API",
        tags=['Tasks'],
        request={
            "title": "nomi",
            "description": "tavsifi",
            "completed":"holati"
        }
    )
    def post(self, request:Request):
        serializer = TodoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)
    

class RegisterView(APIView):
    @extend_schema(
        description="Foydalanuvchini ro'yxatdan o'tkazish uchun API",
        tags=['Auth']
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        password = serializer.data.get('password')
        User.objects.create_user(username=username, password=password)
        return Response({'text':'Royxatdan otdingiz!'})
    

class TodoDetailView(APIView):
    permission_classes=[IsAuthenticated]
    @extend_schema(
        description="Aynan bitta todoni olish uchun API",
        tags=['Tasks']
    )
    def get(self, request:Request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return {{'text':'Todo mavjud emas!'}}
        serializer = TodoSerializer(todo)
        return Response(serializer.data)
    

    @extend_schema(
        description="Todoni yangilash uchun API",
        tags=['Tasks']
    )
    def put(self, request:Request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({'text':'Todo mavjud emas!'})
        serializer = TodoSerializer(todo, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

    @extend_schema(
        description="Todo ni o'chirish uchun API",
        tags=['Tasks']
    )
    def delete(self, request:Request, pk):
        try:
            todo = Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            return Response({'text':'Todo mavjud emas!'})
        todo.delete()
        return Response({'text':'Deleted'})


