# Generated by Django 5.1.2 on 2024-11-03 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('admin', 'Administrator'), ('manager', 'Project Manager'), ('dev', 'Developer'), ('end_user', 'End User')], default='END_USER', max_length=20),
        ),
    ]