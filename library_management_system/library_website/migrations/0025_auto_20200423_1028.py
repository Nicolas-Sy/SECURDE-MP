# Generated by Django 3.0.3 on 2020-04-23 02:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_website', '0024_auto_20200423_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
