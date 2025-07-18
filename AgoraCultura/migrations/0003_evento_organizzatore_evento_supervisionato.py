# Generated by Django 5.2.1 on 2025-06-22 17:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgoraCultura', '0002_rename_video_prime_svolgimento_videoprime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='organizzatore',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='eventi_organizzati', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='evento',
            name='supervisionato',
            field=models.BooleanField(default=False),
        ),
    ]
