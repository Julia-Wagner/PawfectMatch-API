from django.contrib.auth.models import User
from .models import Comment, BannedWord
from rest_framework.test import APITestCase
from rest_framework import status


class CommentListViewTests(APITestCase):
    def setUp(self):
        """
        Set up the testing environment
        """
        self.user = User.objects.create_user(username='test',
                                             password='password')
        self.profile = self.user.profile
        BannedWord.objects.create(word='bannedword1')

    def test_can_list_comments(self):
        """
        Test if a user that is not authenticated can list all comments
        """
        Comment.objects.create(owner=self.user,
                               profile=self.profile,
                               content='A comment')
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_user_can_create_comment(self):
        """
        Test if a logged-in user can create comments
        """
        self.client.login(username='test',
                          password='password')
        response = self.client.post(
            '/comments/',
            {'profile': self.profile.id, 'content': 'New Comment'})
        count = Comment.objects.count()
        self.assertEqual(count, 1)
        created_comment = Comment.objects.first()
        self.assertEqual(str(created_comment), 'New Comment')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_comments(self):
        """
        Test if a user that is not authenticated cannot create comments
        """
        response = self.client.post(
            '/comments/',
            {'profile': self.profile.id, 'content': 'New Comment'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_comment_with_banned_words(self):
        """
        Test if a user cannot create a comment containing a banned word
        """
        self.client.login(username='test',
                          password='password')
        response = self.client.post(
            '/comments/',
            {'profile': self.profile.id,
             'content': 'Comment contains bannedword1'})
        self.assertIn("The word 'bannedword1' is banned. "
                      "Please ensure writing appropriate comments.",
                      response.data['content'])
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_banned_word(self):
        """
        Test if banned words can be created
        """
        banned_word = BannedWord.objects.first()
        self.assertEqual(str(banned_word), 'bannedword1')


class CommentDetailViewTests(APITestCase):
    def setUp(self):
        """
        Set up the testing environment
        """
        self.user = User.objects.create_user(username='test',
                                             password='password')
        self.other_user = User.objects.create_user(username='other',
                                                   password='password')
        self.profile = self.user.profile
        self.comment = Comment.objects.create(owner=self.user,
                                              profile=self.profile,
                                              content='A comment')

    def test_user_can_update_own_comment(self):
        """
        Test if a logged-in user can update their comments
        """
        self.client.login(username='test',
                          password='password')
        response = self.client.put('/comments/1/',
                                   {'content': 'Updated Comment'})
        comment = Comment.objects.filter(pk=1).first()
        self.assertEqual(comment.content, 'Updated Comment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_other_user_comment(self):
        """
        Test if a logged-in user cannot update someone else´s comments
        """
        self.client.login(username='other', password='password')
        response = self.client.put('/comments/1/',
                                   {'content': 'Should Fail'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_comment(self):
        """
        Test if a logged-in user can delete their comments
        """
        self.client.login(username='test', password='password')
        response = self.client.delete('/comments/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cant_delete_another_users_comment(self):
        """
        Test if a logged-in user cannot delete someone else´s comments
        """
        self.client.login(username='other', password='password')
        response = self.client.delete('/comments/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
