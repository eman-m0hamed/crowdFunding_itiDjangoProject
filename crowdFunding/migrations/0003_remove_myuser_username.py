# Generated by Django 4.2.1 on 2023-05-30 00:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crowdFunding', '0002_myuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='username',
        ),
    ]
