# Generated by Django 3.2 on 2021-04-13 19:48

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='This field must contain only letters and spaces.', regex='^[a-z A-Z]*$')], verbose_name='Name')),
                ('last_name', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(message='This field must contain only letters and spaces.', regex='^[a-z A-Z]*$')], verbose_name='Last Name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'ordering': ['-created_at'],
            },
        ),
    ]