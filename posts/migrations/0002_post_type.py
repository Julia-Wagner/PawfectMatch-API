# Generated by Django 3.2.25 on 2024-04-01 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]