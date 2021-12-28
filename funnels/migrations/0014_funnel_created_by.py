# Generated by Django 3.2.9 on 2021-12-28 17:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('funnels', '0013_rename_ongoing_funnel_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='funnel',
            name='created_by',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]