# Generated by Django 3.1.5 on 2021-02-02 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sandwichesweb', '0002_auto_20210202_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='total',
        ),
    ]
