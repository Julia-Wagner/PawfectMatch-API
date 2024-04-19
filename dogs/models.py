from django.db import models
from django.contrib.auth.models import User


class DogCharacteristic(models.Model):
    """
    Separate Characteristics model.
    """
    characteristic = models.CharField(max_length=100)

    def __str__(self):
        return self.characteristic


class Dog(models.Model):
    """
    Dog model.
    Can be inked to multiple posts.
    """
    SIZES = (
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('big', 'Big'),
    )
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='dogs')
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    breed = models.CharField(max_length=250)
    birthday = models.DateField()
    size = models.CharField(max_length=20, choices=SIZES, default='medium')
    gender = models.CharField(max_length=10, choices=GENDER,
                              default='male')
    characteristics = models.ManyToManyField(DogCharacteristic,
                                             related_name='dogs')
    is_adopted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.name}'
