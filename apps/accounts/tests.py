from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


class SignUpTest(TestCase):
    def test_signup_page_loads(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page_redirects_after_signup(self):
        response = self.client.post('/accounts/signup/', {
            'username': 'testuser',
            'password1': 'testpass',
            'password2': 'testpass',
        })
        self.assertEqual(response.status_code, 302)

class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def test_profile_page_loads(self):
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')


class LoginTest(TestCase):
    def test_login_page_loads(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_to_login(self):
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'testpass',
        })
        self.assertEqual(response.status_code, 200)


class LogoutTest(TestCase):
    def test_logout_page_loads(self):
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)


class FollowTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    def follow_user(self):
        response = self.client.post('/api/v1/follow/', {
            'username': 'testuser',
        })
        self.assertEqual(response.status_code, 200)


def UnfollowTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    def unfollow_user(self):
        response = self.client.post('/api/v1/follow/', {
            'username': 'testuser',
        })
        self.assertEqual(response.status_code, 200)


class Profile_view_test(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    def go_to_profile_page(self):
        user = User.objects.get(username='testuser')
        response = self.client.get(f'/accounts/profile/{user.username}/')
        self.assertEqual(response.status_code, 200)
