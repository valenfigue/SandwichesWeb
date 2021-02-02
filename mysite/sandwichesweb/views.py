from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import *

orders_dict = {}

order_list = []
add_ing = []

PRODUCTS_TYPE = [
	"combo",
	"sandwich",
	"drink",
	"side_dish",
]


def reset_orders_dict():
	orders_dict = {  # Para guardar las órdenes sin tener que
		'number': 1,
		'orders': {
			'order_list': [],
			'additional_ing_list': []
		}
	}
	
	return


def index(request):
	return


# return HttpResponse("Hola, mundo. Está en el índice de encuestas.")


class IndexView(generic.ListView):
	template_name = 'sandwichesweb/index.html'
	context_object_name = 'products_list'
	
	def get_queryset(self):
		return None


def order_view(request, order_number=1):
	template = 'sandwichesweb/order.html'
	
	sandwiches_list = Sandwich.objects.filter(is_activated=True).order_by('size')
	drinks_list = Drink.objects.filter(is_activated=True).order_by('name')
	side_dishes_list = SideDish.objects.filter(is_activated=True).order_by('name')
	combo_list = Combo.objects.filter(is_activated=True).order_by('name')
	
	# Generando el pedido
	order = Order(number=order_number)
	order_list.append(order)
	
	context = {
		'sandwiches_list': sandwiches_list,
		'drinks_list': drinks_list,
		'side_dishes_list': side_dishes_list,
		'combo_list': combo_list,
		'order': order,
		# 'type_products': PRODUCTS_TYPE
	}
	
	return render(request, template, context)


def selection(request, product_id, product_type):
	if product_type == 'sandwich':
		selecting_sandwich(request, product_id)
	
	return HttpResponse("Hola, mundo. Está en selection. Opciones elegidas: " +
	                    "Product: " + str(product_type) +
	                    "ID: " + str(product_id))


def selecting_sandwich(request, sandwich_id):
	sandwich = Sandwich.objects.get(pk=sandwich_id)
	cheese = Ingredient.objects.filter(
		name__exact='Queso'.capitalize(),
		is_activated=True
	).get()
	additional_ingredient = Addition(ingredient=cheese, sandwich=sandwich)
	
	order_list[len(order_list) - 1].sandwich = sandwich
	add_ing.append(additional_ingredient)
	
	generating_order(sandwich)
	return HttpResponseRedirect(reverse('sandwichesweb:index'))


class ClientView(generic.FormView):
	template_name = ''
	
	


def generating_order(product):
	# Primero, se crea la orden en la que se guardará el producto recibido.
	order = Order()
	
	# Se calcula el sub_total de la orden con el producto pasado por parámetros
	order.sub_total += product.price
	
	if type(product == 'sandwichesweb.models.Sandwich'):
		order.sandwich_id = product.id
	
	order.save()


# order_list.append(order)


def successful_purchase(order: Order, addition=None):
	order.save()
