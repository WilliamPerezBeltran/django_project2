from django.shortcuts import render
from catalog.models import Category, SubCategory, Product, Alert
import pdb
import datetime

def index(request):
	num_category = Category.objects.all()


	now = datetime.datetime.now()
	alert_roja = Alert.objects.get(id=1)
	alert_amarilla = Alert.objects.get(id=2)
	for product in Product.objects.all():
		expiration_product = str(product.expiration_date)
		expiration_array = expiration_product.split('-')
		expiration_product_year = int(expiration_array[0])
		expiration_product_month = int(expiration_array[1])
		expiration_product_day = int(expiration_array[2])

		current_year = now.year
		current_month = now.month
		current_day = now.day
		if current_year == expiration_product_year and current_month-2 == expiration_product_month and current_month != 1 and current_month != 2:
			print('entro a 1')
			product.alert = alert_roja
			

		if current_year == expiration_product_year and current_month-1 == expiration_product_month and current_month != 1 and current_month != 2:
			print('entro a 2')
			product.alert = alert_amarilla
			

		if current_year-1 == expiration_product_year and current_month == 1:
			print('entro a 3')
			if expiration_product_month == 11:
				print('entro a 4')
				product.alert = alert_roja
				

			if expiration_product_month == 12:
				print('entro a 5')
				product.alert = alert_amarilla
				

		if current_year-1 == expiration_product_year and current_month == 2:
			print('entro a 6')
			if expiration_product_month == 12:
				print('entro a 7')
				product.alert = alert_roja
				

			if expiration_product_month == 1:
				print('entro a 8')
				product.alert = alert_amarilla
				
		# pdb.set_trace()




	num_products = Product.objects.all()


		
    

    
	context = {
		'num_category': num_category,
		'num_products': num_products,
	}

	return render(request, 'index.html', context=context)

def subcategories(request, category_id):
	category = Category.objects.get(pk=category_id)
	context = {
		'category': category,
	}

	return render(request, 'catalog/subcategories.html', context=context)
	# pdb.set_trace()


def products_subcategory(request, sub_category_id):
	subcategory = SubCategory.objects.get(pk=sub_category_id)
	context = {
		'subcategory': subcategory,
	}

	return render(request, 'catalog/products_subcategory.html', context=context)
	# pdb.set_trace()

def product_detalle(request, product_id):
	product = Product.objects.get(pk=product_id)
	context = {
		'product': product,
	}

	return render(request, 'catalog/product_detalle.html', context=context)
	# pdb.set_trace()


