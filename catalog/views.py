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
	# pdb.set_trace()

	now = datetime.datetime.now()
	num_products = Product.objects.all()
	current_date = str(datetime.datetime.now().date())
	num_products_red_alert = {}
	num_products_yellow_alert = {}
	num_expired_products = {}
	# pdb.set_trace()

	# Lógica para encontrar los productos vencidos alertas ojas y alertas amarillas
	for category in num_category:
		subcategories = category.subcategory_set.all()

		contador_products_red_alert = 0
		contador_products_yellow_alert = 0
		contador_expired_products = 0

		for subcategory in subcategories:
			products = subcategory.product_set.all()

			for product in products:
				# pdb.set_trace()
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
	

	context = {
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

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
@login_required
def products(request):

	categories = Category.objects.all()
	all_products = Product.objects.all().order_by('-expiration_date')

	try:
		page = request.GET.get('page', 1)
	except PageNotAnInteger:
		page = 1

	# Provide Paginator with the request object for complete querystring generation
	p = Paginator(all_products, 10)
	products = p.page(page)

	context = {
		'products': products,
		'categories': categories,
		'all_products': all_products,
	}
	return render(request, 'catalog/products.html', context=context)



from django.http import HttpResponse
try:
    import simplejson as json
except ImportError:
    import json
class busqueda_products(generic.TemplateView):

	def get(self, request, *args, **kwargs):

		# pdb.set_trace()
		if request.method == 'GET':
			if request.GET.get('selectCategory'):
				id_category = request.GET['category_id']
				
				products = Product.objects.filter(category__id=id_category)
				category = Category.objects.get(id=id_category)
				subcategories = category.subcategory_set.all()
				result_set = []

				result_set.append({'name':'Eliga una subcategoría' ,'id':''})

				for subcategory in subcategories:
					result_set.append({'name': subcategory.name,'id':subcategory.id})

				data_products = ExtJsonSerializer().serialize(products, fields=['name','category','sub_category','expiration_date','lot','units','alert'])
				data_categories = result_set
				data1 = json.loads(data_products)
				data1.append(data_categories)
				data_response = json.dumps(data1)

				return HttpResponse(data_response, content_type='application/json')

			elif request.GET.get('selectSubCategory'):
				category_id = request.GET.get('category_id')

				subCategory_id = request.GET.get('subCategory_id')
				products = Product.objects.filter(category__id=category_id, sub_category__id=subCategory_id)
				category = Category.objects.get(id=category_id)
				subcategories = category.subcategory_set.all()
				result_set = []

				for subcategory in subcategories:
					result_set.append({'name': subcategory.name,'id':subcategory.id})

				data_products = ExtJsonSerializer().serialize(products, fields=['name','category','sub_category','expiration_date','lot','units','alert'])
				data_categories = result_set
				data1 = json.loads(data_products)
				data1.append(data_categories)
				data_response = json.dumps(data1)

				return HttpResponse(data_response, content_type='application/json')


from django.core.serializers.base import Serializer as BaseSerializer
from django.core.serializers.python import Serializer as PythonSerializer
from django.core.serializers.json import Serializer as JsonSerializer

class ExtBaseSerializer(BaseSerializer):

    def serialize_property(self, obj):
        model = type(obj)
        for field in self.selected_fields:
            if hasattr(model, field) and type(getattr(model, field)) == property:
                self.handle_prop(obj, field)

    def handle_prop(self, obj, field):
        self._current[field] = getattr(obj, field)

    def end_object(self, obj):
        self.serialize_property(obj)

        super(ExtBaseSerializer, self).end_object(obj)


class ExtPythonSerializer(ExtBaseSerializer, PythonSerializer):
    pass


class ExtJsonSerializer(ExtPythonSerializer, JsonSerializer):
    pass