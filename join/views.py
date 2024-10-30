from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, ContactSerializer, TaskSerializer
from rest_framework import status
from .models import Contact, Task, Subtask
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.conf import settings

class LoginView(ObtainAuthToken):
     def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'name': user.username
        })

class GuestLoginView(APIView):
    def post(self, request, *args, **kwargs):
        # Hole Gastdaten aus settings.py, die aus der .env-Datei geladen wurden
        guest_username = settings.GUEST_USERNAME
        guest_password = settings.GUEST_PASSWORD
        guest_email = settings.GUEST_EMAIL

        # Hole oder erstelle den Gast-Benutzer
        guest_user, created = User.objects.get_or_create(
            username=guest_username,
            defaults={'email': guest_email}
        )

        # Setze Passwort nur, falls der Benutzer gerade erstellt wurde
        if created:
            guest_user.set_password(guest_password)
            guest_user.save()

        # Generiere oder hole das Token
        token, _ = Token.objects.get_or_create(user=guest_user)
        return Response({
            'token': token.key,
            'user_id': guest_user.pk,
            'email': guest_user.email,
            'name': guest_user.username
        })

class UserCreate(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def get(self, request, format=None):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = Contact.objects.create(
                name=request.data.get('name', ''), 
                email=request.data.get('email', ''), 
                phone=request.data.get('phone', ''),
                bg_color=request.data.get('bg_color', '#FF7A00'),
                user=request.user
            )
            serialized_obj = serializers.serialize('json', [contact, ]) 
            return HttpResponse(serialized_obj, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        contact = get_object_or_404(Contact, pk=pk)
        serializer = ContactSerializer(contact, data=request.data, partial=True)
        if serializer.is_valid():
            contact = serializer.save()
            serialized_obj = serializers.serialize('json', [contact, ]) 
            return HttpResponse(serialized_obj, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, *args, **kwargs):
        pk = kwargs.get('pk')
        contact = get_object_or_404(Contact, pk=pk)
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class TaskView(APIView):
    serializer_class = TaskSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
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
                dueDate=task_data['dueDate'],
                priority=task_data['priority'],
                category=task_data['category'],
                status=task_data['status']
            )

            contact_ids = request.data.get('assignedTo', [])
            for contact_id in contact_ids:
                try:
                    contact = Contact.objects.get(id=contact_id)
                    task.assignedTo.add(contact)
                except Contact.DoesNotExist:
                    return Response({'error': f"Contact with id {contact_id} does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            subtasks_data = task_data.get('subtasks', [])
            for subtask_data in subtasks_data:
                Subtask.objects.create(task=task, **subtask_data)

            task.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request,*args, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            task = serializer.save()
            serialized_obj = serializers.serialize('json', [task, ]) 
            return HttpResponse(serialized_obj, content_type='application/json')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
            