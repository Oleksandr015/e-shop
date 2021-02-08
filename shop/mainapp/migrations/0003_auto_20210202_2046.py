# Generated by Django 3.1.5 on 2021-02-02 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_notebook_smartphone'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='for_ananymous_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cart',
            name='in_order',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='smartphone',
            name='accum_volume',
            field=models.CharField(max_length=255, verbose_name='Pojemnosc baterii'),
        ),
        migrations.AlterField(
            model_name='smartphone',
            name='display_type',
            field=models.CharField(max_length=255, verbose_name='Rodzaj displeja'),
        ),
        migrations.AlterField(
            model_name='smartphone',
            name='sd',
            field=models.BooleanField(default=True, verbose_name='Dostępność karty SD'),
        ),
        migrations.AlterField(
            model_name='smartphone',
            name='sd_volume_max',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Objętość pamieci'),
        ),
    ]
