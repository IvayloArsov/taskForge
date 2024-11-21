from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .choices import UserRoleChoices
from .forms import CustomUserCreationForm


class AccountsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            first_name='Test',
            last_name='User',
            password='testpass1337'
        )

    def test_user_creation(self):
        """User creation succeeds with correct input"""
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertEqual(self.user.get_full_name(), 'Test User')
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertEqual(self.user.profile.role, UserRoleChoices.END_USER)

    def test_user_creation_invalid_email(self):
        """User creation fails with invalid email """
        form = CustomUserCreationForm(data={
            'email': 'roflcopter@gmail',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass1337',
            'password2': 'testpass1337'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_user_creation_no_email(self):
        """User creation fails without email"""
        form = CustomUserCreationForm(data={
            'email': '',
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'testpass1337',
            'password2': 'testpass1337'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_user_login(self):
        """User can login"""
        login_url = reverse('accounts:login')
        response = self.client.get(login_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(login_url, {
            'username': 'test@test.com',
            'password': 'testpass1337'
        }, follow=True)

        self.assertTrue(response.context['user'].is_authenticated)
        self.assertRedirects(response, reverse('index'))

    def test_user_login_fail(self):
        """Login failure with wrong password"""
        response = self.client.post(reverse('accounts:login'), {
            'username': 'test@test.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
