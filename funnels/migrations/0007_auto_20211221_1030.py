# Generated by Django 3.2.9 on 2021-12-21 05:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('funnels', '0006_added_statusField_in_funnels'),
    ]

    operations = [
        migrations.RenameField(
            model_name='funnel',
            old_name='segment_name',
            new_name='segment',
        ),
        migrations.RenameField(
            model_name='funnel',
            old_name='sub_segment_name',
            new_name='sub_segment',
        ),
    ]
