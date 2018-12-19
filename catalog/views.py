from django.shortcuts import render
from catalog.models import Category, SubCategory, Product
import pdb
import datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic

@login_required
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

@login_required
def subcategories(request, category_id):
	category = Category.objects.get(pk=category_id)
	num_products_red_alert = {}
	num_products_yellow_alert = {}
	num_expired_products = {}

	for subcategory in category.subcategory_set.all():
		contador_products_red_alert = 0
		contador_products_yellow_alert = 0
		contador_expired_products = 0

		for product in subcategory.product_set.all():
			if product.alert == product.RED_ALERT:
				contador_products_red_alert += 1
			elif product.alert == product.YELLOW_ALERT:
				contador_products_yellow_alert += 1
			else:
				contador_expired_products += 1

		num_products_red_alert[subcategory.id] =  contador_products_red_alert
		num_products_yellow_alert[subcategory.id] =  contador_products_yellow_alert
		num_expired_products[subcategory.id] =  contador_expired_products

	context = {
		'num_products_red_alert': num_products_red_alert,
		'num_products_yellow_alert': num_products_yellow_alert,
		'num_expired_products': num_expired_products,
		'category': category,
	}

	return render(request, 'catalog/subcategories.html', context=context)

@login_required
def products_subcategory(request, sub_category_id):
	subcategory = SubCategory.objects.get(pk=sub_category_id)
	subcategory_all_products=subcategory.product_set.all()
	page = request.GET.get(	'page', 1)

	paginator = Paginator(subcategory_all_products, 8)
	try:
		subcategory_all_products = paginator.page(page)
	except PageNotAnInteger:
		subcategory_all_products = paginator.page(1)
	except EmptyPage:
		subcategory_all_products = paginator.page(paginator.num_pages)

	context = {
		'page': page,
		'subcategory_all_products': subcategory_all_products,
		'subcategory': subcategory,
	}

	return render(request, 'catalog/products_subcategory.html', context=context)

@login_required
def product_detalle(request, product_id):
	product = Product.objects.get(pk=product_id)
	context = {
		'product': product,
	}

	return render(request, 'catalog/product_detalle.html', context=context)

class products(generic.ListView):
	model = Category
	context_object_name = 'categories'
	template_name = 'catalog/products.html'


from django.core import serializers
from django.http import HttpResponse
import json
class busqueda_products(generic.TemplateView):

	def get(self, request, *args, **kwargs):
		id_category = request.GET['id']
		products = Product.objects.filter(category__id=id_category)


		
		alerts_product={}
		for product in products:
			alerts_product[product.id] = product.alert

		# data = serializers.serialize('json', products, fields=('name','category','sub_category','expiration_date','lot','units','alert'))
		data = serializers.serialize('json', products)
		data1 = json.loads(data)
		data1.append(alerts_product)
		data_response = json.dumps(data1)
		print('----')
		print(data_response)
		print('----')
		# pdb.set_trace()
		return HttpResponse(data_response, content_type='application/json')



	



