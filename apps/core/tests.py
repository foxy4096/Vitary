from django.test import TestCase, Client

from django.contrib.auth.models import User
from django.contrib.auth import login, logout


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


class PeoplePageTest(TestCase):
    def test_people_page_returns_correct_html(self):
        response = self.client.get('/peoples/')
        self.assertTemplateUsed(response, 'core/peoples.html')
