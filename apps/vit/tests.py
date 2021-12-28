from django.test import TestCase, Client

from django.contrib.auth.models import User

from apps.vit.models import Vit


class VitTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.client.login(username='testuser', password='testpass')

    def test_vit_page_loads(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_add_vit_page_loads(self):
        response = self.client.get('/vit/add/')
        self.assertEqual(response.status_code, 200)

    def test_add_vit_by_adding_a_vit(self):
        self.client.post('/vit/add/', {
            'body': 'Test Vit',
        })
        self.assertEqual(Vit.objects.count(), 1)
        self.assertEqual(Vit.objects.first().body, 'Test Vit')
        self.assertEqual(Vit.objects.first(
        ).user.username, 'testuser')
