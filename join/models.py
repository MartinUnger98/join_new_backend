from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None
    )

    def __str__(self):
        return f'({self.id}) {self.name}'