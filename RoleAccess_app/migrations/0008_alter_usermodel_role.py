# Generated by Django 5.1 on 2025-05-16 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RoleAccess_app', '0007_alter_usermodel_pincode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='role',
            field=models.CharField(max_length=2),
        ),
    ]
