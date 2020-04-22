# Generated by Django 3.0.3 on 2020-04-22 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_website', '0020_remove_comment_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='status',
            field=models.CharField(blank=True, choices=[('a', 'Available'), ('r', 'Reserved')], default='a', help_text='Book availability NOTE: PLEASE SET TO AVAIALBLE IF BOOK IS NOT BORROWED', max_length=1),
        ),
    ]
