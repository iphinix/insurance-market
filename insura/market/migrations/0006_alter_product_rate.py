# Generated by Django 3.2.10 on 2022-02-08 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0005_auto_20220208_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rate',
            field=models.IntegerField(verbose_name='Ставка %'),
        ),
    ]
