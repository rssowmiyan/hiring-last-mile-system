# Generated by Django 3.2.9 on 2021-11-20 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_added_datejoinedfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuser',
            name='start_date',
        ),
    ]
