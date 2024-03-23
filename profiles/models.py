from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    postcode = models.CharField(max_length=255, blank=True)
    country = CountryField(blank=False)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../cgatwxc9v9hkqy4e5kvb'
    )
    type = models.CharField(max_length=255,
                            choices=[("shelter", "Shelter"),
                                     ("adopter", "Adopter")],
                            default="adopter")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(create_profile, sender=User)
