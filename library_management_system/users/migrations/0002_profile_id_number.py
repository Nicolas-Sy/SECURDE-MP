# Generated by Django 3.0.5 on 2020-04-09 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='id_number',
            field=models.CharField(default='', max_length=8),
        ),
    ]
