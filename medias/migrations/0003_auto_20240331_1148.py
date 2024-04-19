# Generated by Django 3.2.25 on 2024-03-31 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0002_media_is_main_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='image',
            field=models.ImageField(blank=True,
                                    default='../default_post_rgq6aq',
                                    null=True, upload_to='post_images/'),
        ),
        migrations.AlterField(
            model_name='media',
            name='type',
            field=models.CharField(choices=[('image', 'Image'),
                                            ('video', 'Video')],
                                   default='image', max_length=20),
        ),
    ]
