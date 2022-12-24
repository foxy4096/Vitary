from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.test import Client, TestCase


class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def check_redirect(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/home/')


