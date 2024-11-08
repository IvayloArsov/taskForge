# Generated by Django 5.1.2 on 2024-11-08 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('admin', 'Administrator'), ('manager', 'Project Manager'), ('dev', 'Developer'), ('end_user', 'End User')], default='end_user', max_length=20),
        ),
    ]
