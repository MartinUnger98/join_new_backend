from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):    
    BG_COLORS = [
        ('#FF7A00', '#FF7A00'),
        ('#462F8A', '#462F8A'),
        ('#FFBB2B', '#FFBB2B'),
        ('#FC71FF', '#FC71FF'),
        ('#6E52FF', '#6E52FF'),
        ('#1FD7C1', '#1FD7C1'),
        ('#9327FF', '#9327FF'),
        ('#FF4646', '#FF4646'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    bg_color = models.CharField(max_length=7, choices=BG_COLORS, default='#FF7A00')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None
    )

    def __str__(self):
        return f'({self.id}) {self.name}'