from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.
def all_products(request):
	"""A view to show all products, inlcuding sorting and search queries"""

	products = Product.objects.all()
	query = None
	categories = None
	sort = None
	direction = None

	if request.GET:
		if 'sort' in request.GET:
			sortkey = request.GET['sort']
			sort = sortkey
			if sortkey == 'name':
				sortkey = 'lower_name'
				products = products.annotate(lower_name=Lower('name'))

			if 'direction' in request:
				direction = request.GET
				if direction == 'desc':
					sortkey = f'-{sortkey}'
			products = products.order_by(sortkey)

		if 'category' in request.GET:
			categories = request.GET['category'].split(',')
			products = products.filter(category__name__in=categories)
			categories = Category.objects.filter(name__in=categories)

		if 'q' in request.GET:
			query = request.GET['q']
			if not query:
				message.error(request, "You didn't enter any search criteria!")
				return redirect(reverse('products'))

			queries = Q(name_icontains=query) | Q(description_icontains=query)
			products = products.filter(queries)

	current_sorting = f'{sort}_{direction}'

	context = {
		'products': products,
		'search_term':query,
		'current_categories': categories,
		'current_sorting': current_sorting,
	}

	return render(request, 'products/products.html', context)


def product_detail(request, product_id):
	"""A view to show individual product detail"""

	product = get_object_or_404(Product, pk=product_id)

	context = {
		'product': product,
	}

	return render(request, 'products/products.html', context)
