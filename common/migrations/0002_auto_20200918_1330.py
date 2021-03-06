# Generated by Django 3.1.1 on 2020-09-18 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='about',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatarPath',
            field=models.CharField(blank=True, max_length=4096),
        ),
        migrations.AlterField(
            model_name='profile',
            name='website',
            field=models.CharField(blank=True, max_length=2048),
        ),
    ]
