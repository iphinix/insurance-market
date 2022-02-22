from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User, UserManager


class Company(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Название компании',
                            unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Логин')
    description = models.TextField(verbose_name='Описание компании')
    email = models.EmailField(verbose_name='E-Mail')
    objects = models.Manager()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name='Продукт')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')
    TYPE_CHOICES = [('Автострахование', 'Автострахование'),
                    ('Недвижимость', 'Недвижимость'),
                    ('Жизнь', 'Жизнь')
                    ]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name='Тип')
    rate = models.IntegerField(verbose_name='Ставка %')
    PERIOD_CHOICES = [('1 месяц', '1 месяц'),
                      ('3 месяца', '3 месяца'),
                      ('6 месяцев', '6 месяцев'),
                      ('1 год', '1 год'),
                      ('3 года', '3 года'),
                      ('5 лет', '5 лет'),
                      ('10 лет', '10 лет'),
                      ]
    period = models.CharField(max_length=30, choices=PERIOD_CHOICES, verbose_name='Период')
    description = models.TextField(verbose_name='Описание продукта')
    objects = models.Manager()

    def __str__(self):
        return self.name


class Response(models.Model):
    name = models.CharField(max_length=50, verbose_name='ФИО')
    email = models.EmailField(verbose_name='E-Mail')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    date_send = models.DateTimeField(default=timezone.now, verbose_name='Время отправки')
    objects = models.Manager()

    def __str__(self):
        return self.name
