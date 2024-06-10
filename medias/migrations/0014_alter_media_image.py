# Generated by Django 3.2.25 on 2024-06-10 18:56

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0013_alter_media_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='../no_image', force_format='WEBP', keep_meta=True, quality=75, scale=None, size=[800, 800], upload_to='images/'),
        ),
    ]
