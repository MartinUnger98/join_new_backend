# join_new_backend-main/your_app/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Contact, Task, Subtask

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username already exists.")
        return value
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        
    def validate_email(self, value):
        if self.instance:
            if Contact.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Email already exists")
        else:
            if Contact.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists")
        return value
    
class SubtaskSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)   
    class Meta:
        model = Subtask
        fields = '__all__'
 
    
class TaskSerializer(serializers.ModelSerializer):
    assignedTo = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True)
    subtasks = SubtaskSerializer(many=True, required=False)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assignedTo', 'dueDate', 'priority', 'category', 'subtasks', 'status']
        
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.dueDate = validated_data.get('dueDate', instance.dueDate)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.category = validated_data.get('category', instance.category)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if 'assignedTo' in validated_data:
            instance.assignedTo.set(validated_data['assignedTo'])

        if 'subtasks' in validated_data:
            subtasks_data = validated_data.pop('subtasks')
            for subtask_data in subtasks_data:
                subtask_id = subtask_data.get('id')
                if subtask_id:
                    subtask = Subtask.objects.get(id=subtask_id, task=instance)
                    subtask.value = subtask_data.get('value', subtask.value)
                    subtask.edit = subtask_data.get('edit', subtask.edit)
                    subtask.save()
                else:
                    Subtask.objects.create(task=instance, **subtask_data)
        
        return instance

