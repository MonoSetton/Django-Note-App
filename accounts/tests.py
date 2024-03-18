from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .views import home, sign_up
from notes.models import Note
from .forms import RegisterForm


class AccountsUrlsTestCase(TestCase):
    def setUp(self):
        self.home_url = reverse('home')
        self.signup_url = reverse('signup')

    def test_home_url(self):
        self.assertEqual(resolve(self.home_url).func, home)

    def test_signup_url(self):
        self.assertEqual(resolve(self.signup_url).func, sign_up)


class AccountsViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.note = Note.objects.create(title='Test Note', body='Test Note Body', author=self.user)
        self.client = Client()
        self.home_url = reverse('home')
        self.signup_url = reverse('signup')

    def test_home_post(self):
        self.client.login(username='testuser', password='password123')
        data = {'note_id': self.note.id}
        response = self.client.post(self.home_url, data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_home_get(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.home_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('notes/home.html')
        self.assertIn('notes', response.context)

    def test_signup_post(self):
        data_register_form = {
            'username': 'testsignup',
            'email': 'testsignupemail@gmail.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123'
        }
        response = self.client.post(self.signup_url, data={
            **data_register_form
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='testsignup').exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, '/home')

    def test_signup_get(self):
        response = self.client.get(self.signup_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTemplateUsed('registration/signup.html')


class AccountsFormsTestCase(TestCase):
    def test_register_form(self):
        form_data = {
            'username': 'testformusername',
            'email': 'testformemail@gmail.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123'
        }
        form = RegisterForm(data=form_data)

        self.assertTrue(form.is_valid())