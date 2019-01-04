from django.urls import path
from . import views

app_name = 'catalog'
urlpatterns = [
	path('',views.index,name='index'),
	path('<int:category_id>',views.subcategories,name='subcategories'),
	path('subcategory/<int:sub_category_id>',views.products_subcategory,name='products_subcategory'),
	path('product/<int:product_id>',views.product_detalle,name='product_detalle'),
	path('products',views.products,name='products'),
	path('busqueda_ajax',views.busqueda_products.as_view(),name='busqueda_products'),
	path('get_import_data',views.get_import_data.as_view(),name='get_import_data'),
	path('import_data',views.import_data,name='import_data'),

]