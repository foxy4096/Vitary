from django.test import TestCase, Client

from django.contrib.auth.models import User

from apps.feed.models import feed


class VitTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def test_feed_page_loads(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_add_feed_page_loads(self):
        response = self.client.get('/feed/add/')
        self.assertEqual(response.status_code, 200)

    def test_add_feed_by_adding_a_feed(self):
        self.client.post('/feed/add/', {
            'body': 'Test feed',
        })
        self.assertEqual(feed.objects.count(), 1)
        self.assertEqual(feed.objects.first().body, 'Test feed')
        self.assertEqual(feed.objects.first(
        ).user.username, 'testuser')
