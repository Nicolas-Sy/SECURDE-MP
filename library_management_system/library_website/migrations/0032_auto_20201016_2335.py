# Generated by Django 3.1.2 on 2020-10-16 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library_website', '0031_remove_historyofborrowers_bookinstance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='book',
            field=models.ForeignKey(help_text='Choose an instance of a book', null=True, on_delete=django.db.models.deletion.CASCADE, to='library_website.book'),
        ),
        migrations.AlterField(
            model_name='bookinstance',
            name='borrower',
            field=models.ForeignKey(blank=True, help_text='[NOTE: PLEASE CHOOSE NULL FIELD IF THERE IS NO BORROWER]', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='historyofborrowers',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='library_website.book'),
        ),
    ]