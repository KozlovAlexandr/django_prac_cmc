# Generated by Django 3.1.1 on 2020-09-27 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20200918_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatarPath',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
