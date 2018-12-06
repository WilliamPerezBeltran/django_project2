from django.shortcuts import render
from catalog.models import Category, SubCategory, Product
import pdb
def index(request):
    num_category = Category.objects.all()
    pdb.set_trace()
    
    context = {
        'num_category': num_category,
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


