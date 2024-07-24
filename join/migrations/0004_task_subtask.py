# Generated by Django 5.0.6 on 2024-07-24 15:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0003_contact_bg_color_alter_contact_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('description', models.CharField(max_length=255)),
                ('dueDate', models.DateField()),
                ('priority', models.CharField(choices=[('Urgent', 'Urgent'), ('Medium', 'Medium'), ('Low', 'Low')], max_length=10)),
                ('category', models.CharField(choices=[('Technical Task', 'Technical Task'), ('User Story', 'User Story'), ('Bug', 'Bug')], max_length=20)),
                ('assignedTo', models.ManyToManyField(related_name='tasks', to='join.contact')),
            ],
        ),
        migrations.CreateModel(
            name='Subtask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255)),
                ('edit', models.BooleanField(default=False)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtasks', to='join.task')),
            ],
        ),
    ]
