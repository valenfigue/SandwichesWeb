#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import date

from django.db import models


class BaseEntity(models.Model):
	"""Entidad base para todos los modelos de la base de datos.
	"""
	# Clases
	class Meta:
		abstract = True
	
	# Atributos comunes en toda la base de datos
	
	# Indica si el registro está activo para ser usado en el sistema. Es una forma para no eliminar el registro en
	# su totalidad.
	is_activated = models.BooleanField(default=True)


class Client(BaseEntity):
	"""Cliente que realiza el pedido.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'sw_client'
		verbose_name = 'Client'
		verbose_name_plural = 'Clients'
	
	# Atributos de la clase:
	id_doc = models.IntegerField(
		"número de identificación",
		unique=True,
		help_text="Por favor, solo ingrese el valor numérico de su número de identificación."
	)
	first_name = models.CharField(
		"primer nombre",
		max_length=30
	)
	middle_name = models.CharField(
		"segundo nombre",
		max_length=30,
		null=True
	)
	surname = models.CharField(
		"primer apellido",
		max_length=30
	)
	second_surname = models.CharField(
		"segundo apellido",
		max_length=30,
		null=True
	)
	
	# Métodos
	def client_name(self) -> str:
		"""Retorna el nombre completo del cliente
		
		:return: nombre completo del cliente.
		:rtype: str
		"""
		complete_name = self.first_name + " " + ((self.middle_name + " ") if self.middle_name else "") + \
			self.surname + ((" " + self.second_surname) if self.second_surname else "")
		
		return complete_name
	
	def __str__(self):
		return str(self.id_doc) + " | " + self.client_name()


class Purchase(BaseEntity):
	"""Compra del cliente
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'sw_purchase'
		verbose_name = 'Purchase'
		verbose_name_plural = 'Purchases'
	
	# Atributos
	date = models.DateTimeField(
		"fecha y hora de compra",
		auto_now_add=True
	)
	total = models.DecimalField(
		"total de la compra",
		max_digits=9,
		decimal_places=2
	)
	
	# Relaciones
	client = models.ForeignKey(
		'Client',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		}
	)


class Product(BaseEntity):
	"""Producto a vender en la tienda.
	
	Esta clase contiene los atributos comunes a todos los productos a usar en el sistema.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		abstract = True
	
	class ListProducts(models.IntegerChoices):
		SANDWICH = 1, 'Sándwich'
		DRINK = 2, 'Bebida'
		SIDE_DISH = 3, 'Acompañante'
		COMBO = 4, 'Combo'
	
	# Atributos
	name = models.CharField(
		"nombre del producto en venta",
		max_length=30
	)
	photo = models.ImageField(
		"foto del producto",
		upload_to='uploads/',
		null=True
	)
	
	# Métodos


class Size(BaseEntity):
	"""Tamaño del sándwich o de la bebida (para esta versión de la aplicación).
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'sw_size'
		verbose_name = 'Size'
		verbose_name_plural = 'Sizes'
	
	class ListProducts(models.IntegerChoices):
		"""Lista de productos que poseen tamaños con precios.
		"""
		SANDWICH = Product.ListProducts.SANDWICH
		DRINK = Product.ListProducts.DRINK
	
	# Atributos
	name = models.CharField(
		"tamaño del producto",
		max_length=30
	)
	product = models.IntegerField(
		"producto",
		choices=ListProducts.choices
	)
	price = models.DecimalField(
		"precio",
		max_digits=9,
		decimal_places=2
	)
	photo = models.ImageField(
		"foto del producto",
		upload_to='uploads/',
		null=True
	)
	
	# Métodos
	def get_product_name(self) -> str:
		"""Obtiene el tipo de producto al que está relacionado este tamaño.
		
		Toma el valor del producto del registro, y lo compara con las opciones de la clase ListProducts, en Size.
		
		:return: El tipo de producto.
		:rtype: str
		"""
		for product in self.ListProducts.choices:
			if self.product == product[0]:
				return product[1]
	
	def __str__(self):
		return self.get_product_name() + " " + self.name
	
	
class Sandwich(Product):
	"""Sándwiches a vender en la tienda.
	"""
	# Clases
	class Meta(Product.Meta):
		db_table = 'sw_sandwich'
		verbose_name = 'Sandwich'
		verbose_name_plural = 'Sandwiches'
	
	# Atributos
	name = None
	type_product = models.IntegerField(
		"producto",
		default=Product.ListProducts.SANDWICH.value
	)
	
	# Relaciones
	size = models.ForeignKey(  # Tamaño del sándwich
		Size,
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True,
			'product': Size.ListProducts.SANDWICH.value
		}
	)
	ingredients = models.ManyToManyField(  # Ingredientes del sándwich.
		'Ingredient',
		through='Addition',
		through_fields=('sandwich', 'ingredient'),
	)
	
	# Métodos
	@staticmethod
	def type_product_name() -> str:
		"""Obtiene el nombre del tipo de producto, de la lista de productos de la clase Product.
		
		:return: Sándwich.
		:rtype: str
		"""
		return Product.ListProducts.SANDWICH.label
		
	def __str__(self):
		return self.type_product_name


class Drink(Product):
	"""Bebidas a vender en la tienda.
	"""
	# Clases
	class Meta(Product.Meta):
		db_table = 'sw_drink'
		verbose_name = 'Drink'
		verbose_name_plural = 'Drinks'
	
	class ListTypeDrinks(models.IntegerChoices):
		SODA = 1, "Refresco"
		JUICE = 2, "Jugo"
		COFFEE = 3, "Café"
		WATER = 4, "Agua"
	
	# Atributos
	type_product = models.IntegerField(
		"producto",
		default=Product.ListProducts.DRINK.value
	)
	type_drink = models.IntegerField(
		"tipo de bebida",
		choices=ListTypeDrinks.choices
	)
	
	# Relaciones
	size = models.ForeignKey(
		Size,
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True,
			'product': Size.ListProducts.DRINK.value
		}
	)
	
	# Métodos
	def get_type_drink_name(self) -> str:
		"""Obtiene el tipo de bebida al que pertenece la instancia.

		Toma el valor del tipo de bebida (type_drink) del registro, y lo compara con las opciones de la clase
		ListTypeDrinks, en Drink.

		:return: El tipo de producto.
		:rtype: str
		"""
		for type_drink in self.ListTypeDrinks:
			if self.type_drink == type_drink[0]:
				return type_drink[1]
	
	@staticmethod
	def type_product_name() -> str:
		"""Obtiene el nombre del tipo de producto, de la lista de productos de la clase Product.

		:return: Bebida.
		:rtype: str
		"""
		return Product.ListProducts.DRINK.label
	
	def __str__(self):
		return self.get_type_drink_name() + ": " + self.name


class SideDish(Product):
	"""Acompañante de sándwich.
	"""
	# Clases
	class Meta(Product.Meta):
		db_table = 'sw_side_dish'
		verbose_name = 'Side Dish'
		verbose_name_plural = 'Side Dishes'
	
	# Atributos
	type_product = models.IntegerField(
		"producto",
		default=Product.ListProducts.SIDE_DISH.value
	)
	price = models.DecimalField(
		"precio",
		max_digits=9,
		decimal_places=2
	)
	
	# Métodos
	@staticmethod
	def type_product_name() -> str:
		"""Obtiene el nombre del tipo de producto, de la lista de productos de la clase Product.

		:return: Acompañante.
		:rtype: str
		"""
		return Product.ListProducts.SIDE_DISH.label
	
	def __str__(self):
		return self.name


class Combo(Product):
	"""Combos en venta
	"""
	# Clases
	class Meta(Product.Meta):
		db_table = 'sw_combo'
		verbose_name = 'Combo'
		verbose_name_plural = 'Combos'
	
	# Atributos
	type_product = models.IntegerField(
		"producto",
		default=Product.ListProducts.COMBO.value
	)
	price = models.DecimalField(
		"precio",
		max_digits=9,
		decimal_places=2
	)
	
	# Relaciones
	sandwiches = models.ManyToManyField(  # Sándwiches del combo.
		'Sandwich',
		through='ProductsInCombo',
		through_fields=('combo', 'sandwich')
	)
	drinks = models.ManyToManyField(
		'Drink',
		through='ProductsInCombo',
		through_fields=('combo', 'drink')
	)
	side_dishes = models.ManyToManyField(
		'SideDish',
		through='ProductsInCombo',
		through_fields=('combo', 'side_dish')
	)
	
	# Métodos
	@staticmethod
	def type_product_name() -> str:
		"""Obtiene el nombre del tipo de producto, de la lista de productos de la clase Product.

		:return: Combo.
		:rtype: str
		"""
		return Product.ListProducts.COMBO.label

	def __str__(self):
		return self.name


class ProductsInCombo(BaseEntity):
	"""Lista de productos incluidos en un combo.
	
	Se trata de un modelo ManyToMany intermediario.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'SW_PRODUCTS_IN_COMBO'.lower()
		verbose_name = 'Products in combo'
		verbose_name_plural = verbose_name
	
	# Atributos

	# Relaciones
	combo = models.ForeignKey(
		'Combo',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True
	)
	sandwich = models.ForeignKey(
		'Sandwich',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True
	)
	drink = models.ForeignKey(
		'Drink',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True
	)
	side_dish = models.ForeignKey(
		'SideDish',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True
	)
	
	# Métodos


class Ingredient(BaseEntity):
	"""Ingredientes que pueden ser agregados a un sándwich.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'SW_INGREDIENT'.lower()
		verbose_name = 'Ingredient'
		verbose_name_plural = 'Ingredients'
	
	# Atributos
	name = models.CharField(
		"nombre",
		max_length=30
	)
	price = models.DecimalField(
		"precio",
		max_digits=9,
		decimal_places=2
	)
	
	# Métodos
	def __str__(self):
		return self.name


class Addition(BaseEntity):
	"""Ingredientes agregados a un sándwich en específico.
	
	Se trata de un modelo ManyToMany intermediario.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'SW_ADDITION'.lower()
		verbose_name = 'Addition'
		verbose_name_plural = 'Additions'
	
	# Atributos
	
	# Relaciones
	ingredient = models.ForeignKey(
		'Ingredient',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		}
	)
	sandwich = models.ForeignKey(
		'Sandwich',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		}
	)


class Order(BaseEntity):
	"""Orden realizada por el cliente.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'sw_order'
		verbose_name = 'Order'
		verbose_name_plural = 'Orders'
	
	# Atributos
	number = models.IntegerField(
		"número del pedido",
		default=1
	)
	# date = models.DateTimeField(
	# 	"fecha y hora de compra",
	# 	auto_now_add=True
	# )
	sub_total = models.DecimalField(
		"sub total",
		max_digits=9,
		decimal_places=2,
		default=0
	)
	
	# Relaciones
	purchase = models.ForeignKey(
		'Purchase',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True
	)
	sandwich = models.ForeignKey(
		'Sandwich',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True
	)
	drink = models.ForeignKey(
		'Drink',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True
	)
	side_dish = models.ForeignKey(
		'SideDish',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True
	)
	combo = models.ForeignKey(
		'Combo',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True
	)


class ScheduleProm(BaseEntity):
	"""Horario de las ofertas.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'SW_SCHEDULE_PROM'.lower()
		verbose_name = 'SCHEDULE'.capitalize()
		verbose_name_plural = 'SCHEDULES'.capitalize()
	
	# Atributos
	start_hour = models.TimeField(  # Hora en el que inicia la oferta, los días seleccionados.
		"hora en el que inicia la oferta"
	)
	end_hour = models.TimeField(  # Hora en el que termina la oferta, los días seleccionados.
		"hora en el que termina la oferta"
	)
	# NOTA: para la versión actual de la aplicación, una oferta debe tener asignada, un horario.
	
	monday = models.BooleanField(
		"lunes",
		default=False
	)
	tuesday = models.BooleanField(
		"martes",
		default=False
	)
	wednesday = models.BooleanField(
		"miércoles",
		default=False
	)
	thursday = models.BooleanField(
		"jueves",
		default=False
	)
	friday = models.BooleanField(
		"viernes",
		default=False
	)
	saturday = models.BooleanField(
		"sábado",
		default=False
	)
	sunday = models.BooleanField(
		"domingo",
		default=False
	)


class Promotion(BaseEntity):
	"""Ofertas de la tienda.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'SW_Promotion'.lower()
		verbose_name = 'Promotion'.capitalize()
		verbose_name_plural = 'Promotions'.capitalize()
	
	# Atributos
	name = models.CharField(
		"nombre de la oferta",
		max_length=48
	)
	description = models.CharField(
		"descripción de la oferta",
		max_length=100,
		null=True
	)
	start_date = models.DateField(
		"fecha en que inicia la oferta",
		default=date.today
	)
	end_date = models.DateField(
		"fecha en que termina la oferta",
		null=True
	)
	discount = models.DecimalField(
		"descuento de la oferta",
		max_digits=3,
		decimal_places=2
	)
	
	# Relaciones
	schedule = models.ForeignKey(
		'ScheduleProm',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		}
	)

	# Métodos
	def prom_is_applicable(self) -> bool:
		"""Verifica si una oferta puede ser todavía aplicable.

		:return: True, si aún no se ha pasado de la fecha final de la oferta.
					De lo contrario, False.
		:rtype: bool
		"""
		today = date.today()
		return today <= self.end_date


class PromApplication(BaseEntity):
	"""Aplicación de una oferta a una orden.
	
	Se trata de un modelo ManyToMany intermediario.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'SW_PROM_APPLICATION'.lower()
		verbose_name = 'PROMOTION APPLICATION'.lower()
		verbose_name_plural = 'PROMOTION APPLICATIONS'.lower()
	
	# Atributos
	
	# Relaciones
	order = models.ForeignKey(
		Order,
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		}
	)
	promotion = models.ForeignKey(
		Promotion,
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		}
	)


class Bill(BaseEntity):
	"""Factura generada por la compra de un cliente.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'SW_BILL'.lower()
		verbose_name = 'Bill'
		verbose_name_plural = 'Bills'
	
	# Atributos
	date = models.DateTimeField(
		"fecha y hora de compra",
		auto_now_add=True
	)
	total = models.DecimalField(
		"total de la compra",
		max_digits=9,
		decimal_places=2
	)
	
	# Relaciones
	purchase = models.OneToOneField(
		'Purchase',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		related_name='purchase',
		related_query_name='purchase',
	)


class QuantityOfProducts(BaseEntity):
	"""Contiene la cantidad de productos de la compra realizada, de acuerdo al tipo de producto.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'SW_QUANTITY_OF_PRODUCTS'.lower()
		verbose_name = 'QUANTITY OF PRODUCTS'.capitalize()
		verbose_name_plural = verbose_name
	
	product = models.CharField(
		"tipo de producto",
		max_length=30
	)
	quantity = models.IntegerField(
		"cantidad de este tipo de producto",
		default=0
	)
	
	# Relaciones
	bill = models.ForeignKey(
		'Bill',
		on_delete=models.CASCADE
	)


class Detail(BaseEntity):
	"""
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'SW_DETAIL'.lower()
		verbose_name = 'Detail'
		verbose_name_plural = 'Details'
	
	# Atributos
	product = models.CharField(
		"tipo de producto",
		max_length=30
	)
	size = models.CharField(
		"tamaño del producto",
		max_length=30,
		null=True
	)
	ingredients = models.CharField(
		"ingredientes del sándwich",
		max_length=100,
		null=True
	)
	price = models.DecimalField(
		"precio del producto",
		max_digits=9,
		decimal_places=2
	)
	
	# Relaciones
	bill = models.ForeignKey(
		'Bill',
		on_delete=models.CASCADE
	)
