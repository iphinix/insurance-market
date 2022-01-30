# Generated by Django 3.2.10 on 2022-01-30 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название компании', max_length=30, verbose_name='Компания')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название продукта', max_length=30, verbose_name='Продукт/Услуга')),
                ('type', models.CharField(choices=[('Автострахование', 'Автострахование'), ('Недвижимость', 'Недвижимость'), ('Жизнь', 'Жизнь')], max_length=50)),
                ('rate', models.CharField(max_length=10)),
                ('period', models.CharField(choices=[('1 месяц', '1 месяц'), ('3 месяца', '3 месяца'), ('6 месяцев', '6 месяцев'), ('12 месяцев', '12 месяцев'), ('1 год', '1 год'), ('3 года', '3 года'), ('5 лет', '5 лет')], max_length=30)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.company')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('mail', models.EmailField(max_length=254)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.company')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.product')),
            ],
        ),
    ]