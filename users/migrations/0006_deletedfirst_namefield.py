# Generated by Django 3.2.9 on 2021-11-21 09:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_addedfirstnamefield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newuser',
            name='first_name',
        ),
    ]
