# Generated by Django 3.0.7 on 2020-06-18 01:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library_website', '0029_auto_20200613_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='historyofborrowers',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='library_website.Book'),
        ),
    ]