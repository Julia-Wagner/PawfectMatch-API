# Generated by Django 3.2.25 on 2024-04-02 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dogs', '0001_initial'),
        ('posts', '0002_post_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dogs',
            field=models.ManyToManyField(related_name='posts', to='dogs.Dog'),
        ),
    ]