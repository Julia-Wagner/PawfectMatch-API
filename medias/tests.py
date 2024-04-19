import os
from datetime import datetime

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from posts.models import Post
from dogs.models import Dog
from .models import Media


class PostMediaListTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user',
                                             password='password')
        self.post = Post.objects.create(title='Test Post',
                                        content='Test content',
                                        owner=self.user)

    def test_can_list_post_medias(self):
        response = self.client.get('/medias/post/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_create_post_media(self):
        self.client.login(username='user', password='password')
        response = self.client.post('/medias/post/1/',
                                    {'name': 'test',
                                     'type': 'image'})
        count = Media.objects.count()
        self.assertEqual(count, 1)
        created_media = Media.objects.first()
        self.assertEqual(str(created_media), 'Media for post 1')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unauthenticated_user_cannot_create_post_media(self):
        response = self.client.post('/medias/post/1/',
                                    {'name': 'test',
                                     'type': 'image'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DogMediaListTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user',
                                             password='password')
        self.shelter_user = User.objects.create_user(username='shelter_user',
                                                     password='password')
        self.shelter_user.profile.type = "shelter"
        self.shelter_user.profile.save()
        self.dog = Dog.objects.create(
            owner=self.user,
            name='Buddy',
            breed='Labrador',
            birthday=datetime.now().strftime("%Y-%m-%d"))

    def test_can_list_dog_medias(self):
        response = self.client.get('/medias/dog/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_shelter_user_can_create_dog_media(self):
        self.client.login(username='shelter_user', password='password')
        response = self.client.post('/medias/dog/1/',
                                    {'name': 'test',
                                     'type': 'image'})
        count = Media.objects.count()
        self.assertEqual(count, 1)
        created_media = Media.objects.first()
        self.assertEqual(str(created_media), 'Media for dog 1')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_regular_user_cannot_create_dog_media(self):
        self.client.login(username='user', password='password')
        response = self.client.post('/medias/dog/1/',
                                    {'name': 'test',
                                     'type': 'image'})
        count = Media.objects.count()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_create_dog_media(self):
        response = self.client.post('/medias/dog/1/',
                                    {'name': 'test',
                                     'type': 'image'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MediaDetailTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user',
                                             password='password')
        self.post = Post.objects.create(title='Test Post',
                                        content='Test content',
                                        owner=self.user)
        self.media = Media.objects.create(owner=self.user,
                                          post=self.post,
                                          name='test')

    def test_can_retrieve_media(self):
        response = self.client.get('/medias/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_owner_can_update_media(self):
        self.client.login(username='user', password='password')
        response = self.client.put('/medias/1/',
                                   {'name': 'updated',
                                    'type': 'image'})
        media = Media.objects.filter(pk=1).first()
        self.assertEqual(media.name, 'updated')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthenticated_user_cannot_update_media(self):
        response = self.client.put('/medias/1/',
                                   {'name': 'updated',
                                    'type': 'image'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_owner_can_delete_media(self):
        self.client.login(username='user', password='password')
        response = self.client.delete('/medias/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unauthenticated_user_cannot_delete_media(self):
        response = self.client.delete('/medias/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
