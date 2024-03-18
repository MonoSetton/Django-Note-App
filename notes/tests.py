from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .views import create_note, update_note, delete_note
from .forms import NoteForm
from .models import Note


class NotesModelTestCase(TestCase):
    def setUp(self):
        self.user = self.user = User.objects.create_user(username='testuser',
                                                         email='test@example.com',
                                                         password='password123')
        self.note = Note.objects.create(title='Test Note', body='Test Note Body', author=self.user)

    def test_note_model(self):
        self.assertEqual(str(self.note), 'Test Note')


class NotesUrlsTestCase(TestCase):
    def setUp(self):
        self.create_note_url = reverse('create_note')
        self.update_note_url = reverse('update_note', args=['1'])
        self.delete_note_url = reverse('delete_note', args=['1'])

    def test_create_note_url(self):
        self.assertEqual(resolve(self.create_note_url).func, create_note)

    def test_update_note_url(self):
        self.assertEqual(resolve(self.update_note_url).func, update_note)

    def test_delete_note_url(self):
        self.assertEqual(resolve(self.delete_note_url).func, delete_note)


class NotesFormsTestCase(TestCase):
    def test_note_form(self):
        form_data = {
            'title': 'Test Note Form',
            'body': 'Test Note Form Body'
        }
        form = NoteForm(data=form_data)

        self.assertTrue(form.is_valid())


class NotesViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.note = Note.objects.create(title='Test Note', body='Test Note Body', author=self.user)
        self.client = Client()
        self.create_note_url = reverse('create_note')
        self.update_note_url = reverse('update_note', args=[self.note.id])
        self.delete_note_url = reverse('delete_note', args=[self.note.id])

    def test_create_note_post(self):
        self.client.login(username='testuser', password='password123')
        note_form_data = {
            'title': 'Test Create Note',
            'body': 'Test Create Note Body'
        }
        response = self.client.post(self.create_note_url, data={
            **note_form_data
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Note.objects.filter(title='Test Create Note').exists())
        self.assertTrue(Note.objects.filter(title='Test Create Note')[0].author == self.user)
        self.assertRedirects(response, '/home')

    def test_create_note_get(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.create_note_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTemplateUsed('notes/create_note.html')

    def test_update_note_post(self):
        self.client.login(username='testuser', password='password123')
        note_form_data = {
            'title': 'Test Update Note',
            'body': 'Test Update Note Body'
        }
        response = self.client.post(self.update_note_url, data={
            **note_form_data
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Note.objects.filter(title='Test Update Note').exists())
        self.assertTrue(Note.objects.filter(body='Test Update Note Body').exists())
        self.assertRedirects(response, '/home')

    def test_update_note_get(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.update_note_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertTemplateUsed('notes/update_note.html')

    def test_delete_note_post(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.delete_note_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Note.objects.filter(title='Test Note').exists())
        self.assertRedirects(response, '/home')

    def test_delete_note_get(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.delete_note_url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('note', response.context)
        self.assertTemplateUsed('notes/delete_note.html')
