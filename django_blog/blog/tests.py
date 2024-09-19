from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import Client

User = get_user_model()

class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'securepassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
    
    def test_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_profile_edit(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('edit_profile'), {
            'first_name': 'Updated',
            'last_name': 'User'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')

    def test_profile_view(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Update Profile')
