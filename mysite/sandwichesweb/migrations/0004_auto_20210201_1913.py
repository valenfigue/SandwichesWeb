# Generated by Django 3.1.5 on 2021-02-01 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sandwichesweb', '0003_auto_20210201_1730'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='combo',
            name='type_product',
        ),
        migrations.RemoveField(
            model_name='drink',
            name='size',
        ),
        migrations.RemoveField(
            model_name='drink',
            name='type_drink',
        ),
        migrations.RemoveField(
            model_name='drink',
            name='type_product',
        ),
        migrations.RemoveField(
            model_name='sandwich',
            name='type_product',
        ),
        migrations.RemoveField(
            model_name='sidedish',
            name='type_product',
        ),
        migrations.AddField(
            model_name='drink',
            name='drink_type',
            field=models.CharField(choices=[('Refresco', 'Refresco'), ('Jugo', 'Jugo'), ('Café', 'Café'), ('Agua', 'Agua')], default='Refresco', max_length=30, verbose_name='tipo de bebida'),
        ),
        migrations.AddField(
            model_name='drink',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='precio'),
        ),
        migrations.AddField(
            model_name='sandwich',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='precio'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='purchase',
            field=models.OneToOneField(limit_choices_to={'is_activated': True}, on_delete=django.db.models.deletion.CASCADE, to='sandwichesweb.purchase'),
        ),
        migrations.AlterField(
            model_name='combo',
            name='name',
            field=models.CharField(help_text="evite usar la palabra 'combo' para dar un nombre. (Ej. 'Chamito').", max_length=30, verbose_name='nombre del combo'),
        ),
        migrations.AlterField(
            model_name='combo',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='precio'),
        ),
        migrations.AlterField(
            model_name='detail',
            name='bill',
            field=models.ForeignKey(limit_choices_to={'is_activated': True}, on_delete=django.db.models.deletion.CASCADE, to='sandwichesweb.bill'),
        ),
        migrations.AlterField(
            model_name='drink',
            name='name',
            field=models.CharField(max_length=30, verbose_name='bebida'),
        ),
        migrations.AlterField(
            model_name='order',
            name='sandwich',
            field=models.ForeignKey(limit_choices_to={'is_activated': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sándwich', related_query_name='sandwich', to='sandwichesweb.sandwich'),
        ),
        migrations.AlterField(
            model_name='quantityofproducts',
            name='bill',
            field=models.ForeignKey(limit_choices_to={'is_activated': True}, on_delete=django.db.models.deletion.CASCADE, to='sandwichesweb.bill'),
        ),
        migrations.AlterField(
            model_name='sandwich',
            name='size',
            field=models.CharField(max_length=30, verbose_name='tamaño del sándwich'),
        ),
        migrations.AlterField(
            model_name='sidedish',
            name='name',
            field=models.CharField(max_length=30, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='sidedish',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='precio'),
        ),
        migrations.DeleteModel(
            name='Size',
        ),
    ]
