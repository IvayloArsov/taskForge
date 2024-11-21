from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Project
from ..accounts.choices import UserRoleChoices


class ProjectTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            first_name='Admin',
            last_name='User',
            password='admin123'
        )
        self.project = Project.objects.create(
            name='Test Project',
            description='Test Description',
            created_by=self.admin_user,
            lead_by=self.admin_user
        )

    def create_user(self, email, first_name, role=None):
        user = get_user_model().objects.create_user(
            email=email,
            first_name=first_name,
            last_name='User',
            password='testpass1337'
        )
        if role:
            user.profile.role = role
            user.profile.save()
            if role == 'manager':
                user.is_staff = True
                user.save()
        return user

    def test_project_creation(self):
        """Project is created with correct info"""
        self.assertEqual(self.project.name, 'Test Project')
        self.assertEqual(self.project.created_by, self.admin_user)

    def test_project_access_permissions(self):
        """Project access based on user role"""
        regular_user = self.create_user('user@test.com', 'Regular')

        # Anonymous user shouldn't access project
        response = self.client.get(reverse('projects:details', args=[self.project.id]))
        self.assertEqual(response.status_code, 302)  # Redirects to login

        # Non-member shouldn't access project
        self.client.login(username='user@test.com', password='testpass1337')
        response = self.client.get(reverse('projects:details', args=[self.project.id]))
        self.assertEqual(response.status_code, 403)  # Forbidden

        # Member should access project
        self.project.members.add(regular_user)
        response = self.client.get(reverse('projects:details', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_manager_can_edit_project(self):
        """Manager can edit project details"""
        self.client.login(username='admin@test.com', password='admin123')

        manager = self.create_user('manager@test.com', 'Manager', 'manager')
        dev_user = self.create_user('dev@test.com', 'Dev', UserRoleChoices.DEVELOPER)
        end_user = self.create_user('user@test.com', 'End', UserRoleChoices.END_USER)

        response = self.client.post(
            reverse('projects:edit', args=[self.project.id]),
            {
                'name': 'Updated Project Name',
                'description': 'Updated Description',
                'lead_by': manager.id,
                'members': [dev_user.id, end_user.id]
            },
            follow=True
        )

        self.project.refresh_from_db()
        self.assertIn(response.status_code, [200, 302])
        self.assertEqual(self.project.name, 'Updated Project Name')

    def test_non_manager_cannot_edit_project(self):
        """Regular user cannot edit project"""
        regular_user = self.create_user('user@test.com', 'Regular')
        self.project.members.add(regular_user)

        self.client.login(username='user@test.com', password='testpass1337')
        response = self.client.post(
            reverse('projects:edit', args=[self.project.id]),
            {
                'name': 'Hacked Project Name',
                'description': 'Hacked Description',
                'lead_by': regular_user.id,
                'members': [regular_user.id]
            }
        )
        self.assertEqual(response.status_code, 403)  # Forbidden
        self.project.refresh_from_db()
        self.assertNotEqual(self.project.name, 'Hacked Project Name')
