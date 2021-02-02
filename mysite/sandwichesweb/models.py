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


# class Client(BaseEntity):
# 	"""Cliente que realiza el pedido.
# 	"""
# 	# Clases
# 	class Meta(BaseEntity.Meta):
# 		db_table = 'sw_client'
# 		verbose_name = 'Cliente'
# 		verbose_name_plural = 'Clientes'
#
# 	# Atributos de la clase:
# 	id_doc = models.IntegerField(
# 		"número de identificación",
# 		unique=True,
# 		help_text="Por favor, solo ingrese el valor numérico de su número de identificación."
# 	)
# 	first_name = models.CharField(
# 		"primer nombre",
# 		max_length=30
# 	)
# 	middle_name = models.CharField(
# 		"segundo nombre",
# 		max_length=30,
# 		null=True
# 	)
# 	surname = models.CharField(
# 		"primer apellido",
# 		max_length=30
# 	)
# 	second_surname = models.CharField(
# 		"segundo apellido",
# 		max_length=30,
# 		null=True
# 	)
#
# 	# Métodos
# 	def client_name(self) -> str:
# 		"""Retorna el nombre completo del cliente
#
# 		:return: nombre completo del cliente.
# 		:rtype: str
# 		"""
# 		complete_name = self.first_name + " " + ((self.middle_name + " ") if self.middle_name else "") + \
# 			self.surname + ((" " + self.second_surname) if self.second_surname else "")
#
# 		return complete_name
#
# 	def __str__(self):
# 		return str(self.id_doc) + " | " + self.client_name()


class Purchase(BaseEntity):
	"""Compra del cliente
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'sw_purchase'
		verbose_name = 'Compra'
		verbose_name_plural = 'Compras'
	
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
	# client = models.ForeignKey(
	# 	'Client',
	# 	on_delete=models.CASCADE,
	# 	limit_choices_to={
	# 		'is_activated': True
	# 	}
	# )


class Product(BaseEntity):
	"""Producto a vender en la tienda.
	
	Esta clase contiene los atributos comunes a todos los productos a usar en el sistema.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		abstract = True
	
	class ListProducts(models.TextChoices):
		SANDWICH = 'Sándwich', 'Sándwich'
		DRINK = 'Bebida', 'Bebida'
		SIDE_DISH = 'Acompañante', 'Acompañante'
		COMBO = 'Combo', 'Combo'
	
	# Atributos
	price = models.DecimalField(
		"precio",
		max_digits=9,
		decimal_places=2,
		default=0
	)
	photo = models.ImageField(
		"foto del producto",
		upload_to='uploads/',
		null=True
	)
	
	# Métodos


class Sandwich(Product):
	"""Sándwiches a vender en la tienda.
	"""
	# Clases
	class Meta(Product.Meta):
		db_table = 'sw_sandwich'
		verbose_name = 'Sándwich'
		verbose_name_plural = 'Sándwiches'
	
	# Atributos
	size = models.CharField(
		"tamaño del sándwich",
		max_length=30
	)
	
	# Relaciones
	ingredients = models.ManyToManyField(  # Ingredientes del sándwich.
		'Ingredient',
		through='Addition',
		through_fields=('sandwich', 'ingredient'),
		# related_name='ingredientes del sándwich',
		# related_query_name='ingredients'
	)
	
	# Métodos
	@staticmethod
	def product_type_name() -> str:
		"""Obtiene el nombre del tipo de producto, de la lista de productos de la clase Product.
		
		:return: Sándwich.
		:rtype: str
		"""
		return Product.ListProducts.SANDWICH.label
		
	def __str__(self):
		return self.product_type_name() + " " + self.size


class Drink(Product):
	"""Bebidas a vender en la tienda.
	"""
	# Clases
	class Meta(Product.Meta):
		db_table = 'sw_drink'
		verbose_name = 'Bebida'
		verbose_name_plural = 'Bebidas'
	
	class ListDrinkType(models.TextChoices):
		SODA = 'Refresco', 'Refresco',
		JUICE = 'Jugo', 'Jugo',
		COFFEE = 'Café', 'Café',
		WATER = 'Agua', 'Agua',
	
	# Atributos
	name = models.CharField(
		"bebida",
		max_length=30
	)
	drink_type = models.CharField(
		"tipo de bebida",
		max_length=30,
		choices=ListDrinkType.choices,
		default=ListDrinkType.SODA.value,
	)
	# size = models.CharField(
	# 	"tamaño de la bebida",
	# 	max_length=30
	# )
	
	# Relaciones
	
	# Métodos
	@staticmethod
	def product_type_name() -> str:
		"""Obtiene el nombre del tipo de producto, de la lista de productos de la clase Product.

		:return: Bebida.
		:rtype: str
		"""
		return Product.ListProducts.DRINK.label
	
	def __str__(self):
		return self.drink_type + ": " + self.name


class SideDish(Product):
	"""Acompañante de sándwich.
	"""
	# Clases
	class Meta(Product.Meta):
		db_table = 'sw_side_dish'
		verbose_name = 'Acompañante'
		verbose_name_plural = 'Acompañantes'
	
	# Atributos
	name = models.CharField(
		"nombre",
		max_length=30
	)
	
	# Métodos
	@staticmethod
	def product_type_name() -> str:
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
	name = models.CharField(
		"nombre del combo",
		max_length=30,
		help_text="evite usar la palabra 'combo' para dar un nombre. (Ej. 'Chamito')."
	)
	
	# Relaciones
	sandwiches = models.ManyToManyField(  # Sándwiches del combo.
		'Sandwich',
		through='ProductsInCombo',
		through_fields=('combo', 'sandwich'),
		# related_name='sandwiches del combo',
		# related_query_name='sandwiches'
	)
	drinks = models.ManyToManyField(
		'Drink',
		through='ProductsInCombo',
		through_fields=('combo', 'drink'),
		# related_name='bebidas del combo',
		# related_query_name='drinks'
	)
	side_dishes = models.ManyToManyField(
		'SideDish',
		through='ProductsInCombo',
		through_fields=('combo', 'side_dish'),
		# related_name='acompañantes del combo',
		# related_query_name='side_dishes'
	)
	
	# Métodos
	@staticmethod
	def product_type_name() -> str:
		"""Obtiene el nombre del tipo de producto, de la lista de productos de la clase Product.

		:return: Combo.
		:rtype: str
		"""
		return Product.ListProducts.COMBO.label

	def __str__(self):
		return self.product_type_name() + self.name


class ProductsInCombo(BaseEntity):
	"""Lista de productos incluidos en un combo.
	
	Se trata de un modelo ManyToMany intermediario.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'SW_PRODUCTS_IN_COMBO'.lower()
		verbose_name = 'Productos en combo'
		verbose_name_plural = verbose_name
		
		# constraints = [
		# 	models.CheckConstraint(
		# 		name="%(app_label)s_%(class)s_product_included",
		# 		check=(
		# 			models.Q(
		# 				sandwich__isnull=False,
		# 				drink__isnull=True,
		# 				side_dish__isnull=True,
		# 			),
		# 			models.Q(
		# 				sandwich__isnull=True,
		# 				drink__isnull=False,
		# 				side_dish__isnull=True,
		# 			),
		# 			models.Q(
		# 				sandwich__isnull=True,
		# 				drink__isnull=True,
		# 				side_dish__isnull=False,
		# 			)
		# 		),
		# 	)
		# ]
	
	# Atributos

	# Relaciones
	combo = models.ForeignKey(
		'Combo',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True,
		# related_name='combo',
		# related_query_name='combo'
	)
	sandwich = models.ForeignKey(
		'Sandwich',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True,
		# related_name='sándwich',
		# related_query_name='sandwich'
	)
	drink = models.ForeignKey(
		'Drink',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True,
		# related_name='bebida',
		# related_query_name='drink',
	)
	side_dish = models.ForeignKey(
		'SideDish',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True,
		# related_name='acompañante',
		# related_query_name='side_dish'
	)
	
	# Métodos


class Ingredient(BaseEntity):
	"""Ingredientes que pueden ser agregados a un sándwich.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'SW_INGREDIENT'.lower()
		verbose_name = 'Ingrediente'
		verbose_name_plural = 'Ingredientes'
	
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
		verbose_name = 'Adicional'
		verbose_name_plural = 'Adicionales'
	
	# Atributos
	
	# Relaciones
	ingredient = models.ForeignKey(
		'Ingredient',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		# related_name='ingrediente',
		# related_query_name='ingredient'
	)
	sandwich = models.ForeignKey(
		'Sandwich',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		# related_name='sándwich',
		# related_query_name='sandwich'
	)


class Order(BaseEntity):
	"""Orden realizada por el cliente.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'sw_order'
		verbose_name = 'Pedido'
		verbose_name_plural = 'Pedidos'
	
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
		null=True,
		# related_name='compra',
		# related_query_name='purchase'
	)
	sandwich = models.ForeignKey(
		'Sandwich',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True,
		related_name='sándwich',
		related_query_name='sandwich'
	)
	drink = models.ForeignKey(
		'Drink',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True,
		# related_name='bebida',
		# related_query_name='drink'
	)
	side_dish = models.ForeignKey(
		'SideDish',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True,
		# related_name='acompañante',
		# related_query_name='side_dish'
	)
	combo = models.ForeignKey(
		'Combo',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		null=True,
		# related_name='combo',
		# related_query_name='combo'
	)


class ScheduleProm(BaseEntity):
	"""Horario de las ofertas.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'SW_SCHEDULE_PROM'.lower()
		verbose_name = 'Horario'
		verbose_name_plural = 'Horarios'
	
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
		verbose_name = 'Oferta'
		verbose_name_plural = 'Ofertas'
	
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
		},
		# related_name='horario de la oferta',
		# related_query_name='schedule'
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
		verbose_name = 'Aplicación de oferta'.lower()
		verbose_name_plural = 'Aplicaciones de oferta'.lower()
	
	# Atributos
	
	# Relaciones
	order = models.ForeignKey(
		Order,
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		# related_name='pedido al que se le aplicó la oferta',
		# related_query_name='order'
	)
	promotion = models.ForeignKey(
		Promotion,
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		# related_name='oferta aplicada',
		# related_query_name='promotion'
	)


class Bill(BaseEntity):
	"""Factura generada por la compra de un cliente.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'SW_BILL'.lower()
		verbose_name = 'Factura'
		verbose_name_plural = 'Facturas'
	
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
	
	# Atributos relacionados con el cliente
	ci_client = models.IntegerField(
		"número de identificación del cliente",
		# unique=True,
		help_text="Por favor, solo ingrese el valor numérico de su número de identificación.",
		# default=0,
	)
	first_name_client = models.CharField(
		"primer nombre del cliente",
		max_length=30
	)
	middle_name_client = models.CharField(
		"segundo nombre del cliente",
		max_length=30,
		null=True
	)
	surname_client = models.CharField(
		"primer apellido del cliente",
		max_length=30
	)
	second_surname_client = models.CharField(
		"segundo apellido del cliente",
		max_length=30,
		null=True
	)
	
	# Relaciones
	purchase = models.OneToOneField(
		'Purchase',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		# related_name='compra',
		# related_query_name='purchase',
	)


class QuantityOfProducts(BaseEntity):
	"""Contiene la cantidad de productos de la compra realizada, de acuerdo al tipo de producto.
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'SW_QUANTITY_OF_PRODUCTS'.lower()
		verbose_name = 'Cantidad de productos comprados'
		verbose_name_plural = verbose_name
	
	product = models.CharField(
		"tipo de producto",
		max_length=30,
		choices=Product.ListProducts.choices,
		default=Product.ListProducts.SANDWICH.value
	)
	quantity = models.IntegerField(
		"cantidad de este tipo de producto",
		default=0
	)
	
	# Relaciones
	bill = models.ForeignKey(
		'Bill',
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		# related_name='factura',
		# related_query_name='bill'
	)


class Detail(BaseEntity):
	"""
	"""
	# Clases
	class Meta(BaseEntity.Meta):
		db_table = 'SW_DETAIL'.lower()
		verbose_name = 'Detalle de factura'
		verbose_name_plural = 'Detalles de factura'
	
	# Atributos
	product = models.CharField(
		"tipo de producto",
		max_length=30,
		choices=Product.ListProducts.choices,
		default=Product.ListProducts.SANDWICH.value
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
		on_delete=models.CASCADE,
		limit_choices_to={
			'is_activated': True
		},
		# related_name='factura',
		# related_query_name='bill'
	)
