# Generated by Django 3.0.3 on 2020-04-17 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_website', '0014_auto_20200415_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='reviews',
            field=models.TextField(default='', help_text='Enter your review of the book', max_length=1000),
        ),
    ]
