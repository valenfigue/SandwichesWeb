# Generated by Django 3.1.5 on 2021-02-02 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sandwichesweb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='sandwich',
        ),
        migrations.AddField(
            model_name='addition',
            name='order',
            field=models.ForeignKey(limit_choices_to={'is_activated': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', related_query_name='order', to='sandwichesweb.order'),
        ),
    ]
