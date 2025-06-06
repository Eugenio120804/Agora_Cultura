# Generated by Django 5.2.1 on 2025-05-28 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AgoraCultura', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='svolgimento',
            old_name='video_prime',
            new_name='videoprime',
        ),
        migrations.AlterUniqueTogether(
            name='svolgimento',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='evento',
            name='categorie',
            field=models.ManyToManyField(through='AgoraCultura.Associazione', to='AgoraCultura.categoria'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='prezzo',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='prenotazione',
            name='data_prenotazione',
            field=models.DateField(auto_now_add=True),
        ),
    ]
