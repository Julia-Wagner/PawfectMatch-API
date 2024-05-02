from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Follower


class FollowerListViewTests(APITestCase):
    def setUp(self):
        """
        Set up the testing environment
        """
        self.user = User.objects.create_user(username='user1',
                                             password='password')
        self.other_user = User.objects.create_user(username='user2',
                                                   password='password')
        self.third_user = User.objects.create_user(username='user3',
                                                   password='password')

    def test_can_list_followers(self):
        """
        Test if a logged-in user can list all followers
        """
        Follower.objects.create(owner=self.user, followed=self.other_user)
        self.client.login(username='user1', password='password')
        response = self.client.get('/followers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_follower(self):
        """
        Test if a logged-in user can add a follow
        """
        self.client.login(username='user1', password='password')
        response = self.client.post('/followers/',
                                    {'followed': self.other_user.id})
        self.assertEqual(Follower.objects.count(), 1)
        created_follow = Follower.objects.first()
        self.assertEqual(str(created_follow), 'user1 user2')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_followers(self):
        """
        Test if a user that is not authenticated cannot add a follow
        """
        response = self.client.post('/followers/',
                                    {'followed': self.other_user.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_follow_twice(self):
        """
        Test if a user cannot follow the same user twice
        """
        self.client.login(username='user1', password='password')
        self.client.post('/followers/',
                         {'followed': self.other_user.id})
        response = self.client.post('/followers/',
                                    {'followed': self.other_user.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'possible duplicate', status_code=400)


class FollowerDetailViewTests(APITestCase):
    def setUp(self):
        """
        Set up the testing environment
        """
        self.user = User.objects.create_user(username='user1',
                                             password='password')
        self.other_user = User.objects.create_user(username='user2',
                                                   password='password')
        Follower.objects.create(owner=self.user, followed=self.other_user)

    def test_user_can_delete_own_follower(self):
        """
        Test if a user can delete a follow
        """
        self.client.login(username='user1', password='password')
        response = self.client.delete('/followers/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Follower.objects.count(), 0)

    def test_user_cant_delete_another_users_follower(self):
        """
        Test if a user cannot delete another user´s follow
        """
        self.third_user = User.objects.create_user(username='user3',
                                                   password='password')
        self.client.login(username='user3', password='password')
        response = self.client.delete('/followers/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
