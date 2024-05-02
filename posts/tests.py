from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        """
        Set up the testing environment
        """
        User.objects.create_user(username='test', password='password')

    def test_can_list_posts(self):
        """
        Test if a user that is not authenticated can list all posts
        """
        tester = User.objects.get(username='test')
        Post.objects.create(owner=tester, title='test title')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_post(self):
        """
        Test if a logged-in user can create posts
        """
        self.client.login(username='test', password='password')
        response = self.client.post('/posts/', {'title': 'test title'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        created_post = Post.objects.first()
        self.assertEqual(str(created_post), '1 test title')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_post(self):
        """
        Test if a user that is not authenticated cannot create posts
        """
        response = self.client.post('/posts/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        """
        Set up the testing environment
        """
        tester = User.objects.create_user(username='test', password='password')
        other = User.objects.create_user(username='other', password='password')
        Post.objects.create(
            owner=tester, title='test title', content='tester content'
        )
        Post.objects.create(
            owner=other, title='another title', content='other tester content'
        )

    def test_can_retrieve_post_using_valid_id(self):
        """
        Test if a user can get a post with a valid id
        """
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'test title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_post_using_invalid_id(self):
        """
        Test if a user cannot get a post with an invalid id
        """
        response = self.client.get('/posts/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_post(self):
        """
        Test if a logged-in user can update their post
        """
        self.client.login(username='test', password='password')
        response = self.client.put('/posts/1/', {'title': 'a new title'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_post(self):
        """
        Test if a logged-in user cannot update another user´s post
        """
        self.client.login(username='test', password='password')
        response = self.client.put('/posts/2/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_post(self):
        """
        Test if a logged-in user can delete their post
        """
        self.client.login(username='test', password='password')
        response = self.client.delete('/posts/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_another_users_post(self):
        """
        Test if a logged-in user cannot delete another user´s post
        """
        self.client.login(username='test', password='password')
        response = self.client.delete('/posts/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
