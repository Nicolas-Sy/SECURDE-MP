# Generated by Django 3.0.7 on 2020-06-13 14:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('library_website', '0028_auto_20200613_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyofborrowers',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID', primary_key=True, serialize=False),
        ),
    ]
