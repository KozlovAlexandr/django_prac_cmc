# Generated by Django 3.1.1 on 2020-09-18 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paste', '0007_auto_20200918_1832'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='paste',
            name='paste_paste_creatio_d67108_idx',
        ),
        migrations.AddIndex(
            model_name='paste',
            index=models.Index(fields=['creation_date'], name='paste_paste_creatio_a112a9_idx'),
        ),
        migrations.AddIndex(
            model_name='paste',
            index=models.Index(fields=['expiration_date'], name='paste_paste_expirat_15eaf8_idx'),
        ),
    ]
