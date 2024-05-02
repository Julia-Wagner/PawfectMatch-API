from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime
from .models import Dog, DogCharacteristic


class DogListViewTests(APITestCase):
    def setUp(self):
        """
        Set up the testing environment
        """
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
        """
        Test if a user that is not authenticated can list all dogs
        """
        response = self.client.get('/dogs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_shelter_user_can_create_dog(self):
        """
        Test if a logged-in shelter user can create dogs
        """
        self.client.login(username='shelter_user', password='password')
        response = self.client.post(
            '/dogs/', {'name': 'Stella',
                       'breed': 'Mix',
                       'birthday': datetime.now().strftime("%Y-%m-%d")})
        count = Dog.objects.count()
        self.assertEqual(count, 2)
        created_dog = Dog.objects.first()
        self.assertEqual(str(created_dog), '2 Stella')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_dog(self):
        """
        Test if a user that is not authenticated cannot create dogs
        """
        response = self.client.post(
            '/dogs/', {'name': 'Stella',
                       'breed': 'Mix',
                       'birthday': datetime.now().strftime("%Y-%m-%d")})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_cannot_create_dog(self):
        """
        Test if a user that is not a shelter cannot create dogs
        """
        self.client.login(username='user', password='password')
        response = self.client.post(
            '/dogs/', {'name': 'Stella',
                       'breed': 'Mix',
                       'birthday': datetime.now().strftime("%Y-%m-%d")})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DogDetailViewTests(APITestCase):
    def setUp(self):
        """
        Set up the testing environment
        """
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
        """
        Test if a dog can be retrieved with a valid id
        """
        response = self.client.get('/dogs/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_dog_using_invalid_id(self):
        """
        Test if a dog cannot be retrieved with an invalid id
        """
        response = self.client.get('/dogs/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_shelter_user_can_update_own_dog(self):
        """
        Test if a logged-in shelter user can update their dog
        """
        self.client.login(username='shelter_user', password='password')
        response = self.client.put(
            '/dogs/1/', {'name': 'Buddy 2',
                         'breed': 'Labrador',
                         'birthday': datetime.now().strftime("%Y-%m-%d")})
        dog = Dog.objects.filter(pk=1).first()
        self.assertEqual(dog.name, 'Buddy 2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_not_logged_in_cant_update_dog(self):
        """
        Test if a user that is not authenticated cannot update a dog
        """
        response = self.client.put(
            '/dogs/1/', {'name': 'Buddy 2',
                         'breed': 'Labrador',
                         'birthday': datetime.now().strftime("%Y-%m-%d")})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_cant_update_dog(self):
        """
        Test if a user that is not a shelter cannot update a dog
        """
        self.client.login(username='user', password='password')
        response = self.client.put(
            '/dogs/1/', {'name': 'Buddy 2',
                         'breed': 'Labrador',
                         'birthday': datetime.now().strftime("%Y-%m-%d")})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_shelter_user_can_delete_own_dog(self):
        """
        Test if a logged-in shelter user can delete their dog
        """
        self.client.login(username='shelter_user', password='password')
        response = self.client.delete('/dogs/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_not_logged_in_cant_delete_dog(self):
        """
        Test if a user that is not authenticated cannot delete a dog
        """
        response = self.client.delete('/dogs/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_cannot_delete_dog(self):
        """
        Test if a user that is not a shelter cannot delete a dog
        """
        self.client.login(username='user', password='password')
        response = self.client.delete('/dogs/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DogCharacteristicListViewTests(APITestCase):
    def setUp(self):
        """
        Set up the testing environment
        """
        self.user = User.objects.create_user(username='user',
                                             password='password')
        self.shelter_user = User.objects.create_user(username='shelter_user',
                                                     password='password')
        self.shelter_user.profile.type = "shelter"
        self.shelter_user.profile.save()
        self.dog_characteristic = DogCharacteristic.objects.create(
            characteristic='Friendly')

    def test_can_list_dog_characteristics(self):
        """
        Test if a user can list all dog characteristics
        """
        response = self.client.get('/dogs/characteristics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DogCharacteristicDetailViewTests(APITestCase):
    def setUp(self):
        """
        Set up the testing environment
        """
        self.user = User.objects.create_user(username='user',
                                             password='password')
        self.shelter_user = User.objects.create_user(username='shelter_user',
                                                     password='password')
        self.shelter_user.profile.type = "shelter"
        self.shelter_user.profile.save()
        self.dog_characteristic = DogCharacteristic.objects.create(
            characteristic='Friendly')

    def test_can_retrieve_dog_characteristic_using_valid_id(self):
        """
        Test if a dog characteristic can be retrieved with a valid id
        """
        response = self.client.get('/dogs/characteristics/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_dog_characteristic_using_invalid_id(self):
        """
        Test if a dog characteristic cannot be retrieved with an invalid id
        """
        response = self.client.get('/dogs/characteristics/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
