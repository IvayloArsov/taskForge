from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Ticket
from ..projects.models import Project
from ..accounts.choices import UserRoleChoices


class TicketTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.admin = get_user_model().objects.create_superuser(
            email='admin@test.com',
            first_name='Admin',
            last_name='User',
            password='admin123'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            created_by=self.admin,
            lead_by=self.admin
        )

    def create_user(self, email, first_name, role=None):
        """Helper method to create users with specific roles"""
        user = get_user_model().objects.create_user(
            email=email,
            first_name=first_name,
            last_name='User',
            password='testpass1337'
        )
        if role:
            user.profile.role = role
            user.profile.save()
        return user

    def test_developer_can_create_ticket(self):
        """Developer can create ticket successfully"""
        dev_user = self.create_user('dev@test.com', 'Dev', UserRoleChoices.DEVELOPER)
        self.project.members.add(dev_user)

        self.client.login(username='dev@test.com', password='testpass1337')
        response = self.client.post(
            reverse('tickets:create'),
            {
                'title': 'Test Ticket',
                'description': 'Test Description',
                'priority': 'medium',
                'status': 'open',
                'project': self.project.id,
                'assigned_to': dev_user.id,
                'due_date': '2024-12-31'
            },
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Ticket.objects.filter(title='Test Ticket').exists())

    def test_developer_can_edit_own_ticket(self):
        """Developer can edit their own ticket"""
        dev_user = self.create_user('dev@test.com', 'Dev', UserRoleChoices.DEVELOPER)
        self.project.members.add(dev_user)

        ticket = Ticket.objects.create(
            title='Original Title',
            description='Original Description',
            priority='low',
            status='open',
            project=self.project,
            created_by=dev_user,
            assigned_to=dev_user
        )

        self.client.login(username='dev@test.com', password='testpass1337')
        response = self.client.post(
            reverse('tickets:edit', args=[ticket.id]),
            {
                'title': 'Updated Title',
                'description': 'Updated Description',
                'priority': 'high',
                'status': 'in_progress',
                'project': self.project.id,
                'assigned_to': dev_user.id,
                'due_date': '2024-12-31'
            },
            follow=True
        )

        ticket.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ticket.title, 'Updated Title')
        self.assertEqual(ticket.status, 'in_progress')

    def test_developer_can_delete_own_ticket(self):
        """Developer can delete their own ticket"""
        dev_user = self.create_user('dev@test.com', 'Dev', UserRoleChoices.DEVELOPER)
        self.project.members.add(dev_user)

        ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            priority='low',
            status='open',
            project=self.project,
            created_by=dev_user,
            assigned_to=dev_user
        )

        self.client.login(username='dev@test.com', password='testpass1337')
        response = self.client.post(
            reverse('tickets:delete', args=[ticket.id]),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Ticket.objects.filter(id=ticket.id).exists())