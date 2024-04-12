from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime
from .models import Dog


class DogListViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user',
                                             password='password')
        self.shelter_user = User.objects.create_user(username='shelter_user',
                                                     password='password')
        self.shelter_user.profile.type = "shelter"
        self.shelter_user.profile.save()
        self.dog = Dog.objects.create(
            owner=self.shelter_user,
            name='Buddy',
            breed='Labrador',
            birthday=datetime.now().strftime("%Y-%m-%d"))

    def test_can_list_dogs(self):
        response = self.client.get('/dogs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shelter_user_can_create_dog(self):
        self.client.login(username='shelter_user', password='password')
        response = self.client.post(
            '/dogs/', {'name': 'Stella',
                       'breed': 'Mix',
                       'birthday': datetime.now().strftime("%Y-%m-%d")})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_dog(self):
        response = self.client.post(
            '/dogs/', {'name': 'Stella',
                       'breed': 'Mix',
                       'birthday': datetime.now().strftime("%Y-%m-%d")})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_cannot_create_dog(self):
        self.client.login(username='user', password='password')
        response = self.client.post(
            '/dogs/', {'name': 'Stella',
                       'breed': 'Mix',
                       'birthday': datetime.now().strftime("%Y-%m-%d")})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DogDetailViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user',
                                             password='password')
        self.shelter_user = User.objects.create_user(username='shelter_user',
                                                     password='password')
        self.shelter_user.profile.type = "shelter"
        self.shelter_user.profile.save()
        self.dog = Dog.objects.create(
            owner=self.shelter_user,
            name='Buddy',
            breed='Labrador',
            birthday=datetime.now().strftime("%Y-%m-%d"))

    def test_can_retrieve_dog_using_valid_id(self):
        response = self.client.get('/dogs/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_dog_using_invalid_id(self):
        response = self.client.get('/dogs/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_shelter_user_can_update_own_dog(self):
        self.client.login(username='shelter_user', password='password')
        response = self.client.put(
            f'/dogs/1/', {'name': 'Buddy 2',
                          'breed': 'Labrador',
                          'birthday': datetime.now().strftime("%Y-%m-%d")})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_not_logged_in_cant_update_dog(self):
        response = self.client.put(
            f'/dogs/1/', {'name': 'Buddy 2',
                          'breed': 'Labrador',
                          'birthday': datetime.now().strftime("%Y-%m-%d")})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_cannot_update_dog(self):
        self.client.login(username='user', password='password')
        response = self.client.put(
            f'/dogs/1/', {'name': 'Buddy 2',
                          'breed': 'Labrador',
                          'birthday': datetime.now().strftime("%Y-%m-%d")})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_shelter_user_can_delete_own_dog(self):
        self.client.login(username='shelter_user', password='password')
        response = self.client.delete(f'/dogs/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_not_logged_in_cant_delete_dog(self):
        response = self.client.delete('/dogs/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_cannot_delete_dog(self):
        self.client.login(username='user', password='password')
        response = self.client.delete('/dogs/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
