from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, Role

class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        # Create a role for the user
        Role.objects.create(name='regular')

    def test_user_registration(self):
        url = reverse('register')  
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
        }
        
        #Send a POST request to the registration endpoint
        response = self.client.post(url, data, format='json')

        #Check that the user is created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 
        
        #Check that the user was created in the database
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())  # Check that the user exists in the database

    def test_user_registration_missing_fields(self):
        url = reverse('register')
        data = {
            'username': '',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
        }
        response = self.client.post(url, data, format='json')
       
       # Check for bad request due to missing username
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  