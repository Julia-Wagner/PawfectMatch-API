from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from saves.models import Save
from posts.models import Post


class SaveListViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1',
                                             password='password')
        self.post = Post.objects.create(title="Sample Post",
                                        owner=self.user)
        self.other_user = User.objects.create_user(username='user2',
                                                   password='password')

    def test_list_saves(self):
        Save.objects.create(owner=self.user, post=self.post)
        self.client.login(username='user1', password='password')
        response = self.client.get('/saves/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_save(self):
        self.client.login(username='user1', password='password')
        response = self.client.post('/saves/', {'post': self.post.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Save.objects.count(), 1)

    def test_user_not_logged_in_cant_create_save(self):
        response = self.client.post('/saves/', {'post': self.post.id})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SaveDetailViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1',
                                             password='password')
        self.post = Post.objects.create(title="Sample Post",
                                        owner=self.user)
        self.save = Save.objects.create(owner=self.user, post=self.post)
        self.other_user = User.objects.create_user(username='user2',
                                                   password='password')

    def test_retrieve_save(self):
        self.client.login(username='user1', password='password')
        response = self.client.get('/saves/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_own_save(self):
        self.client.login(username='user1', password='password')
        response = self.client.delete('/saves/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Save.objects.count(), 0)

    def test_user_cant_delete_another_users_save(self):
        self.client.login(username='user2', password='password')
        response = self.client.delete('/saves/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
