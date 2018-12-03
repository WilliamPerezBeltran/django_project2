from django.db import models

# Create your models here.

from django.urls import reverse  # To generate URLS by reversing URL patterns


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        help_text="Ingresa la categoría"
        )

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=200, help_text="Ingresa la sub-categoría")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, help_text="Nombre del producto")
    date = models.DateField(max_length=256, help_text="Fecha de fabricación")
    expiration_date = models.DateField(max_length=256, help_text="Fecha de vencimiento")
    lot = models.CharField(max_length=200, help_text="Lote del producto")
    units = models.PositiveIntegerField(help_text="Cantidad recibida")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.SET_NULL, null=True)

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

