from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Comment
from ..tickets.models import Ticket
from ..projects.models import Project
from ..accounts.choices import UserRoleChoices


class CommentTest(TestCase):
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

        self.dev_user = get_user_model().objects.create_user(
            email='dev@test.com',
            first_name='Dev',
            last_name='User',
            password='testpass1337'
        )
        self.dev_user.profile.role = UserRoleChoices.DEVELOPER
        self.dev_user.profile.save()
        self.project.members.add(self.dev_user)

        self.ticket = Ticket.objects.create(
            title='Test Ticket',
            description='Test Description',
            priority='medium',
            status='open',
            project=self.project,
            created_by=self.dev_user,
            assigned_to=self.dev_user
        )

    def test_user_can_comment(self):
        """Project member can add comment to ticket"""
        self.client.login(username='dev@test.com', password='testpass1337')

        response = self.client.post(
            reverse('comments:create', args=[self.ticket.id]),
            {'content': 'Test comment content'},
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        comment = Comment.objects.filter(ticket=self.ticket).first()
        self.assertIsNotNone(comment)
        self.assertEqual(comment.content, 'Test comment content')
        self.assertEqual(comment.author, self.dev_user)

    def test_user_can_delete_own_comment(self):
        """Member can delete their own comment"""
        comment = Comment.objects.create(
            ticket=self.ticket,
            author=self.dev_user,
            content='Test comment to delete'
        )

        self.client.login(username='dev@test.com', password='testpass1337')
        response = self.client.post(
            reverse('comments:delete', args=[comment.id]),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())
        self.assertRedirects(response,
                             reverse('tickets:details', args=[self.ticket.id]))
