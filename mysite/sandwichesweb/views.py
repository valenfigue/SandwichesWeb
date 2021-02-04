from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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


def index_view(request):
	template = 'sandwichesweb/index.html'
	
	promotions_list = Promotion.objects.filter(is_activated=True)
	
	context = {
		'promotions_list': promotions_list,
	}
	
	return render(request, template, context)


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


def selection(request):
	product_id = request.POST['product_id']
	product_type = request.POST['product_type']
	decision = request.POST['decision']
	
	if product_type == 'sandwich':
		selecting_sandwich(request, product_id)

	return HttpResponseRedirect(reverse('sandwichesweb:client', args=()))


# def selection(request, product_id, product_type, decision):
# 	if product_type == 'sandwich':
# 		selecting_sandwich(request, product_id)
# 	# else:
#
# 	if decision == 1:
# 		order_list[len(order_list) - 1].number += 1


def selecting_sandwich(request, sandwich_id):
	sandwich = Sandwich.objects.get(pk=sandwich_id)
	cheese = Ingredient.objects.filter(
		name__exact='Queso'.capitalize(),
		is_activated=True
	).get()
	
	order = order_list[len(order_list) - 1]
	order.sub_total = sandwich.price + cheese.price
	
	additional_ingredient = Addition(ingredient=cheese, sandwich=sandwich, order=order)
	add_ing.append(additional_ingredient)


def client_view(request):
	template = 'sandwichesweb/client.html'
	
	return render(request, template, {})


def bill_view(request):
	ci = request.POST['ci']
	first_name = request.POST['first_name'].upper()
	middle_name = request.POST['middle_name'].upper()
	surname = request.POST['surname'].upper()
	second_surname = request.POST['second_surname'].upper()
	
	bill = Bill(
		ci_client=ci,
		first_name_client=first_name,
		middle_name_client=middle_name,
		surname_client=surname,
		second_surname_client=second_surname,
	)
	
	bill = successful_purchase(bill)
	billing(bill)
	qops = QuantityOfProducts.objects.filter(bill=bill)
	details = Detail.objects.filter(bill=bill)
	
	order_list.clear()
	add_ing.clear()
	
	return HttpResponse("lo lograste: " +
	                    "bill: " + str(bill.id)
	                    )
	# return HttpResponse("Hola, nuevo cliente: " +
	#                     "ci: " + str(ci) +
	#                     "first_name: " + first_name +
	#                     "middle_name: " + middle_name +
	#                     "surname: " + surname +
	#                     "second_surname: " + second_surname)


def billing(bill):
	orders_bill = Order.objects.filter(purchase=bill.purchase)
	
	sandwiches_count = 0
	drinks_count = 0
	side_dishes_count = 0
	combos_count = 0
	for order in orders_bill:
		detail = Detail(bill=bill)
		
		# Contando los sándwiches de ese pedido
		additional_ings = Addition.objects.filter(order=order)
		if additional_ings:
			sandwiches_count += 1
			detail.product = Product.ListProducts.SANDWICH.label
			
			n = 1
			for ing in additional_ings:
				if n == 1:
					detail.ingredients += " "
				else:
					if n == additional_ings.count():
						detail.ingredients += "y "
					else:
						detail.ingredients += ", "
				detail.ingredients += ing.ingredient.name
				n += 1
				
				if n == additional_ings.count():
					detail.size = ing.sandwich.size
		elif order.drink_id:
			drinks_count += 1
			drink = order.drink
			
			detail.product = Product.ListProducts.DRINK.label
			detail.name = drink.name
		elif order.side_dish_id:
			side_dishes_count += 1
			side_dish = order.side_dish
			
			detail.product = Product.ListProducts.SIDE_DISH.label
			detail.name = side_dish.name
		elif order.combo_id:
			combos_count += 1
			combo = order.combo
			
			detail.product = Product.ListProducts.COMBO.label
			detail.name = combo.name
		detail.price = order.sub_total
		detail.save()
	
	# Cantidad por tipo de producto
	if sandwiches_count:
		qop = QuantityOfProducts(bill=bill)
		qop.product = Product.ListProducts.SANDWICH.label
		qop.quantity = sandwiches_count
		qop.save()
	if drinks_count:
		qop = QuantityOfProducts(bill=bill)
		qop.product = Product.ListProducts.DRINK.label
		qop.quantity = drinks_count
		qop.save()
	if side_dishes_count:
		qop = QuantityOfProducts(bill=bill)
		qop.product = Product.ListProducts.SIDE_DISH.label
		qop.quantity = side_dishes_count
		qop.save()
	if combos_count:
		qop = QuantityOfProducts(bill=bill)
		qop.product = Product.ListProducts.COMBO.label
		qop.quantity = combos_count
		qop.save()


def successful_purchase(bill: Bill):
	purchase = Purchase()
	purchase.save()
	
	bill.total = 0
	for order in order_list:
		bill.total += order.sub_total
		order.save()
		
	for ingredient in add_ing:  # guardando las
		ingredient.save()
	
	bill.purchase = purchase
	bill.save()
	
	return bill
