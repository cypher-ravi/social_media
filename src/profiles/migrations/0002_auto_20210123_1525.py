# Generated by Django 3.1.5 on 2021-01-23 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='no bio...', max_length=300),
        ),
    ]
