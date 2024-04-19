# Generated by Django 3.2.25 on 2024-03-23 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                                           primary_key=True,
                                           serialize=False,
                                           verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=255)),
                ('address_1', models.CharField(blank=True, max_length=255)),
                ('address_2', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('postcode', models.CharField(blank=True, max_length=255)),
                ('country', django_countries.fields.CountryField(
                    max_length=2)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(
                    default='../cgatwxc9v9hkqy4e5kvb', upload_to='images/')),
                ('type', models.CharField(choices=[('shelter', 'Shelter'),
                                                   ('adopter', 'Adopter')],
                                          default='adopter', max_length=255)),
                ('owner', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
