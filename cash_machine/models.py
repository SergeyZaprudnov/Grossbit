from django.db import models


class Item(models.Model):
    """Описание модели товара"""
    title = models.CharField(max_length=150, verbose_name='Наименование')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Стоимость')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
