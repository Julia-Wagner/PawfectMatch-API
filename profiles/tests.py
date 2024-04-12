from django.contrib.auth.models import User
from .models import Profile
from rest_framework import status
from rest_framework.test import APITestCase


class ProfileListTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             password='password')

    def test_can_list_profiles(self):
        response = self.client.get('/profiles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ProfileDetailTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             password='password')

    def test_can_retrieve_profile(self):
        self.client.login(username='test', password='password')
        response = self.client.get('/profiles/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_update_own_profile(self):
        self.client.login(username='test', password='password')
        response = self.client.put('/profiles/1/', {'name': 'Updated Name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_cannot_update_other_profile(self):
        self.client.login(username='other', password='password')
        response = self.client.put('/profiles/1/',
                                   {'name': 'Updated Name'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
