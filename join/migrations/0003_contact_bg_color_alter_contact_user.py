# Generated by Django 5.0.6 on 2024-06-19 19:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0002_contact_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='bg_color',
            field=models.CharField(choices=[('#FF7A00', '#FF7A00'), ('#462F8A', '#462F8A'), ('#FFBB2B', '#FFBB2B'), ('#FC71FF', '#FC71FF'), ('#6E52FF', '#6E52FF'), ('#1FD7C1', '#1FD7C1'), ('#9327FF', '#9327FF'), ('#FF4646', '#FF4646')], default='#FF7A00', max_length=7),
        ),
        migrations.AlterField(
            model_name='contact',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]