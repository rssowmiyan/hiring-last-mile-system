# Generated by Django 3.2.9 on 2021-12-20 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funnels', '0005_funnel_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='funnel',
            name='ongoing',
            field=models.BooleanField(default=False),
        ),
    ]
