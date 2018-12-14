from django.shortcuts import render
from catalog.models import Category, SubCategory, Product
import pdb
import datetime
from datetime import timedelta
# from catalog.models import RED_ALERT, YELLOW_ALERT, EXPIRED_PRODUCT


def index(request):
	num_category = Category.objects.all()

	now = datetime.datetime.now()
	num_products = Product.objects.all()
	current_date = str(datetime.datetime.now().date())
	
	num_products_red_alert = {}
	num_products_yellow_alert = {}
	num_expired_products = {}

	# Lógica para encontrar los productos vencidos alertas ojas y alertas amarillas
	for category in num_category:
		subcategories = category.subcategory_set.all()

		contador_products_red_alert = 0
		contador_products_yellow_alert = 0
		contador_expired_products = 0

		for subcategory in subcategories:
			products = subcategory.product_set.all()

			for product in products:
				if product.alert == product.RED_ALERT:
					contador_products_red_alert += 1
				elif product.alert == product.YELLOW_ALERT:
					contador_products_yellow_alert += 1
				else:
					contador_expired_products += 1

				

		num_products_red_alert[category.id] = contador_products_red_alert
		num_products_yellow_alert[category.id] = contador_products_yellow_alert
		num_expired_products[category.id] = contador_expired_products



				
			

	
	# Lógica para encontrar el total de productos que tiene una categoria 
	num_products_by_category={}
	for category in num_category:
		subcategories = category.subcategory_set.all()
		subcategory_products_num = 0

		for subcategory in subcategories:
			subcategory_products_num += subcategory.product_set.count()

		num_products_by_category[category.id] = subcategory_products_num

			

	

	
	context = {
		'num_products_red_alert': num_products_red_alert,
		'num_products_yellow_alert': num_products_yellow_alert,
		'num_expired_products': num_expired_products,
		'num_products_by_category': num_products_by_category,
		'current_date': current_date,
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


def products(request):
	num_products = Product.objects.all()
	context = {
		'num_products': num_products,
	}

	return render(request, 'catalog/products.html', context=context)
	# pdb.set_trace()


