from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core import serializers as django_serializers
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.conf import settings

from .models import Contact, Task, Subtask
from .serializers import UserSerializer, ContactSerializer, TaskSerializer, CustomAuthTokenSerializer
from .utils import update_subtasks


class LoginView(ObtainAuthToken):
    """
    Authenticates a user and returns a token with basic user info.
    """
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'name': user.username
        })


class GuestLoginView(APIView):
    """
    Provides access for a guest user using predefined credentials.
    """
    def post(self, request, *args, **kwargs):
        guest_user, created = User.objects.get_or_create(
            username=settings.GUEST_USERNAME,
            defaults={'email': settings.GUEST_EMAIL}
        )
        if created:
            guest_user.set_password(settings.GUEST_PASSWORD)
            guest_user.save()

        token, _ = Token.objects.get_or_create(user=guest_user)
        return Response({
            'token': token.key,
            'user_id': guest_user.pk,
            'email': guest_user.email,
            'name': guest_user.username
        })


class UserCreate(APIView):
    """
    Creates a new user using the UserSerializer.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactView(APIView):
    """
    Handles CRUD operations for contacts. Requires authentication.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = serializer.save(user=request.user)
            serialized_obj = django_serializers.serialize('json', [contact])
            return HttpResponse(serialized_obj, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        contact = get_object_or_404(Contact, pk=pk)
        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            contact = serializer.save()
            serialized_obj = django_serializers.serialize('json', [contact])
            return HttpResponse(serialized_obj, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        contact = get_object_or_404(Contact, pk=pk)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskView(APIView):
    """
    Handles CRUD operations for tasks, including nested subtasks and assigned contacts.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task_data = serializer.validated_data
            task = Task.objects.create(
                title=task_data['title'],
                description=task_data['description'],
                due_date=task_data['due_date'],
                priority=task_data['priority'],
                category=task_data['category'],
                status=task_data['status']
            )
            contact_ids = request.data.get('assigned_to', [])
            contacts = Contact.objects.filter(id__in=contact_ids)
            task.assigned_to.set(contacts)
            subtasks_data = task_data.get('subtasks', [])
            update_subtasks(task, subtasks_data)
            task.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            task = serializer.save()
            serialized_obj = django_serializers.serialize('json', [task])
            return HttpResponse(serialized_obj, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
