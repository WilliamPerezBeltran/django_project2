from django.urls import path
from . import views

app_name = 'catalog'
urlpatterns = [
	path('',views.index,name='index'),
	path('<int:category_id>',views.subcategories,name='subcategories'),
	path('subcategory/<int:sub_category_id>',views.products_subcategory,name='products_subcategory'),
	path('product/<int:product_id>',views.product_detalle,name='product_detalle'),
	path('products',views.products,name='products'),

]