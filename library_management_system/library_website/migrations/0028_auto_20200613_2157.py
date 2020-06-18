# Generated by Django 3.0.7 on 2020-06-13 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library_website', '0027_historyofborrowers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historyofborrowers',
            name='book',
        ),
        migrations.AddField(
            model_name='historyofborrowers',
            name='bookInstance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='library_website.BookInstance'),
        ),
    ]