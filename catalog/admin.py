from django.contrib import admin

from catalog.models import Category, SubCategory, Product

# admin.site.register(Category)
# admin.site.register(SubCategory)
# admin.site.register(Product)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','category')
    list_filter = ('name', 'category')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','date','expiration_date','lot','units','category','sub_category')
    list_filter = ('date','expiration_date','category','sub_category')
    # fields = ['name',('lot','units'),('sub_category','category')]
    fieldsets = (
        (None, {
            'fields': ['name',('lot','units'),('sub_category','category')]
        }),
        ('Date', {
            'fields': ('date','expiration_date')
        }),
    )