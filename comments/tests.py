from django.contrib.auth.models import User
from .models import Comment
from rest_framework.test import APITestCase
from rest_framework import status


class CommentListViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             password='password')
        self.profile = self.user.profile
        self.banned_words = ['bannedword1',
                             'bannedword2']

    def test_can_list_comments(self):
        Comment.objects.create(owner=self.user,
                               profile=self.profile,
                               content='A comment')
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_comment(self):
        self.client.login(username='test',
                          password='password')
        response = self.client.post(
            '/comments/',
            {'profile': self.profile.id, 'content': 'New Comment'})
        count = Comment.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_comments(self):
        response = self.client.post(
            '/comments/',
            {'profile': self.profile.id, 'content': 'New Comment'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_comment_with_banned_words(self):
        self.client.login(username='test',
                          password='password')
        response = self.client.post(
            '/comments/',
            {'text': 'Comment contains bannedword1'})
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)


class CommentDetailViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test',
                                             password='password')
        self.other_user = User.objects.create_user(username='other',
                                                   password='password')
        self.profile = self.user.profile
        self.comment = Comment.objects.create(owner=self.user,
                                              profile=self.profile,
                                              content='A comment')

    def test_user_can_update_own_comment(self):
        self.client.login(username='test',
                          password='password')
        response = self.client.put(f'/comments/1/',
                                   {'content': 'Updated Comment'})
        comment = Comment.objects.filter(pk=1).first()
        self.assertEqual(comment.content, 'Updated Comment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_other_user_comment(self):
        self.client.login(username='other', password='password')
        response = self.client.put(f'/comments/1/',
                                   {'content': 'Should Fail'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_comment(self):
        self.client.login(username='test', password='password')
        response = self.client.delete('/comments/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_another_users_comment(self):
        self.client.login(username='other', password='password')
        response = self.client.delete('/comments/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
