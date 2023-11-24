from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


class SignUpTest(TestCase):
    def test_signup_page_loads(self):
        response = self.client.get('/account/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page_redirects_after_signup(self):
        response = self.client.post('/account/signup/', {
            'username': 'testuser',
            'password1': 'testpass',
            'password2': 'testpass',
        })
        self.assertEqual(response.status_code, 302)

class UserProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def test_userprofile_page_loads(self):
        response = self.client.get('/account/userprofile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/userprofile.html')


class LoginTest(TestCase):
    def test_login_page_loads(self):
        response = self.client.get('/account/login/')
        self.assertEqual(response.status_code, 200)

    def test_to_login(self):
        response = self.client.post('/account/login/', {
            'username': 'testuser',
            'password': 'testpass',
        })
        self.assertEqual(response.status_code, 200)


class LogoutTest(TestCase):
    def test_logout_page_loads(self):
        response = self.client.get('/account/logout/')
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


class user_detail_test(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    def go_to_userprofile_page(self):
        user = User.objects.get(username='testuser')
        response = self.client.get(f'/account/userprofile/{user.username}/')
        self.assertEqual(response.status_code, 200)
