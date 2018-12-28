from django.db import models
from django.urls import reverse  
import datetime
from datetime import timedelta
import pdb

class Category(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Ingresa la categoría"
        )
    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=200, help_text="Ingresa la sub-categoría")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    RED_ALERT    = 'red_alert'
    YELLOW_ALERT = 'yellow_alert'
    EXPIRED_PRODUCT = 'vencido'

    name = models.CharField(max_length=200, help_text="Nombre del producto")
    date = models.DateField(max_length=256, help_text="Fecha de fabricación")
    expiration_date = models.DateField(max_length=256, help_text="Fecha de vencimiento")
    lot = models.CharField(max_length=200, help_text="Lote del producto")
    units = models.PositiveIntegerField(help_text="Cantidad recibida")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])

    @property
    def alert(self):
        expiration_red = self.expiration_date - timedelta(days=30)
        expiration_yellow = self.expiration_date - timedelta(days=60)
        current_date = datetime.datetime.now().date()

        if current_date >= self.expiration_date:
            return self.EXPIRED_PRODUCT 
        elif current_date >= expiration_red:
            return self.RED_ALERT
        elif current_date >= expiration_yellow:
            return self.YELLOW_ALERT

    @classmethod
    def expired(self):
        return self.objects.filter(expiration_date__lte=datetime.date.today())

    def __str__(self):
        return self.name

