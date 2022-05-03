from django.test import TestCase, Client

from django.contrib.auth.models import User
from apps.notification.models import Notification


class NotificationTestCast(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
        )
        user2 = User.objects.create_user(
            username='testuser2',
            password='testpass',
        )
        self.client.login(username='testuser', password='testpass')
        self.client.post('/accounts/follow/', {'username': user2.username})
        
    def test_notification_page_loads(self):
        response = self.client.get('/notification/')
        self.assertEqual(response.status_code, 200)
