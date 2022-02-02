from django.db import models
#from django.contrib.auth.models import User, UserManager


class Company(models.Model):
    name = models.CharField(max_length=30,
                            help_text='Введите название компании',
                            verbose_name='Компания')
    objects = models.Manager()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=30,
                            #help_text='Введите название продукта',
                            verbose_name='Продукт/Услуга')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    TYPE_CHOICES = [('Автострахование', 'Автострахование'),
                    ('Недвижимость', 'Недвижимость'),
                    ('Жизнь', 'Жизнь')
                    ]
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    rate = models.CharField(max_length=10)
    PERIOD_CHOICES = [('1 месяц', '1 месяц'),
                      ('3 месяца', '3 месяца'),
                      ('6 месяцев', '6 месяцев'),
                      ('12 месяцев', '12 месяцев'),
                      ('1 год', '1 год'),
                      ('3 года', '3 года'),
                      ('5 лет', '5 лет')
                      ]
    period = models.CharField(max_length=30, choices=PERIOD_CHOICES)
    objects = models.Manager()

    def __str__(self):
        return self.name


class Response(models.Model):
    name = models.CharField(max_length=40)
    mail = models.EmailField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return self.name
