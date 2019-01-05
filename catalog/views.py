from django.shortcuts import render
from catalog.models import Category, SubCategory, Product
import pdb
import datetime
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import generic
import openpyxl

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
		category_id = request.GET.get('category_id')
		
		subCategory_id = request.GET.get('subCategory_id')
		if len(request.GET) == 1:
			print('esta en categorias')
			products = Product.objects.filter(category__id=category_id)
		else:
			print('esta en subCategory')
			products = Product.objects.filter(category__id=category_id, sub_category__id=subCategory_id)

		category = Category.objects.get(id=category_id)
		subcategories = category.subcategory_set.all()
		data_categories = []

		for subcategory in subcategories:
			if str(subcategory.id) == str(subCategory_id):
				data_categories.append({'name': subcategory.name,'id':subcategory.id,'subcategory_id_selected': True})
			else:
				data_categories.append({'name': subcategory.name,'id':subcategory.id})

		data_products = ExtJsonSerializer().serialize(products, fields=['name','category','sub_category','expiration_date','lot','units','alert'])
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

@login_required
def import_data(request):

	context = {
	}
	return render(request, 'catalog/import_data.html', context=context)	

try:
    import simplejson as json
except ImportError:
    import json
class get_import_data(generic.TemplateView):
	def post(self, request, *args, **kwargs):
		response_data = {'modal': 'success'};

		categories = Category.objects.all()
		sub_categories = SubCategory.objects.all()
		all_categories = list()
		all_sub_categories = list()
		for category in categories:
			all_categories.append(category.name)
		for sub_category in sub_categories:
			all_sub_categories.append(sub_category.name)
		
		excel_file = request.FILES["excel_file"]
		# you may put validations here to check extension or file size
		wb = openpyxl.load_workbook(excel_file)
		# getting a particular sheet by name out of many sheets
		worksheet = wb["Hoja1"]
		print(worksheet)
		excel_data = list()
		excel_dict = {
			'name': '', 
			'date': '', 
			'expiration_date': '', 
			'lot': '', 
			'units': '', 
			'category': '', 
			'sub_category': '', 
			}
		# iterating over the rows and
		# getting value from each cell in row
		for row in worksheet.iter_rows():
			row_data = list()
			excel_dict = {
			'name': '', 
			'date': '', 
			'expiration_date': '', 
			'lot': '', 
			'units': '', 
			'category': '', 
			'sub_category': '', 
			}

			for cell in row:
				row_data.append(str(cell.value))

			excel_dict['name'] = row_data[0]
			date = row_data[1].split(' ')
			excel_dict['date'] = date[0]
			expiration_date = row_data[2].split(' ')
			excel_dict['expiration_date'] = expiration_date[0]
			excel_dict['lot'] = row_data[3]
			excel_dict['units'] = row_data[4]
			# valido que la categoria ingresada en el excel exista en la base de datos 
			if row_data[5] in all_categories:
				category_excel = Category.objects.get(name=row_data[5])
				excel_dict['category'] = category_excel
				print('fue verdadero ')
				print(row_data[5])
				print('fue verdadero ')
				print(row_data[5])
			else:
				response_data = {
					'modal': 'error',
					'data_error': row_data[5],
					'error_in': 'categorías',
					};
				data_response = json.dumps(response_data)
				return HttpResponse(data_response, content_type='application/json')

			# valido que la subcategoria ingresada en el excel exista en la base de datos 
			if row_data[6] in all_sub_categories:
				sub_category_excel = SubCategory.objects.get(name=row_data[6])
				excel_dict['sub_category'] = sub_category_excel
				print('fue verdadero ')
				print(row_data[6])
				print('fue verdadero ')
				print(row_data[6])
			else:
				response_data = {'modal': 'data error in excel '};
				response_data = {
					'modal': 'error',
					'data_error': row_data[6],
					'error_in': 'subcategorias',
					};
				data_response = json.dumps(response_data)
				return HttpResponse(data_response, content_type='application/json')
				break
			try:
				Product.objects.create(name=excel_dict['name'],date =excel_dict['date'] ,expiration_date =excel_dict['expiration_date'] ,lot =excel_dict['lot'] ,units =excel_dict['units'] ,category =excel_dict['category'] ,sub_category =excel_dict['sub_category'] )
			except Exception as e:
				logging.error('Error in data')
				logging.error(e)

			excel_data.append(excel_dict)
		# data1 = json.loads(response_data)
		data_response = json.dumps(response_data)
		return HttpResponse(data_response, content_type='application/json')


		


		

	

	

