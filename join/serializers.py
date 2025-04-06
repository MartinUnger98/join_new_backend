from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Contact, Task, Subtask
from .utils import update_subtasks


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Django's built-in User model.
    Handles creation and validation of new users with password hashing.
    """
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        
    def validate_username(self, value):
        """
        Ensures that the username is unique.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username already exists.")
        return value
    
    def validate_email(self, value):
        """
        Ensures that the email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists.")
        return value

    def create(self, validated_data):
        """
        Creates a new user with a hashed password.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email']
        )
        return user

class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for the Contact model.
    Handles validation to ensure unique email addresses.
    """
    class Meta:
        model = Contact
        fields = '__all__'
        
    def validate_email(self, value):
        """
        Ensures that the email is unique across contacts, allowing updates.
        """
        if self.instance:
            if Contact.objects.filter(email=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("Email already exists")
        else:
            if Contact.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email already exists")
        return value
    
class SubtaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subtask model.
    Used as a nested serializer in tasks.
    """
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all(), required=False)
    class Meta:
        model = Subtask
        fields = '__all__'
        
class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    Includes nested subtasks and many-to-many assigned contacts.
    """
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True)
    subtasks = SubtaskSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_to', 'due_date',
                  'priority', 'category', 'subtasks', 'status']

    def update(self, instance, validated_data):
        """
        Updates task fields, assigned contacts, and nested subtasks.
        Delegates subtask logic to a utility function.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.category = validated_data.get('category', instance.category)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if 'assigned_to' in validated_data:
            instance.assigned_to.set(validated_data['assigned_to'])

        if 'subtasks' in validated_data:
            update_subtasks(instance, validated_data.pop('subtasks'))

        return instance