from django.urls import path

from . import views


app_name = 'sandwichesweb'
urlpatterns = [
	# path('', views.index, name='index'),
	path('', views.IndexView.as_view(), name='index'),
	path('order/', views.order_view, name='order'),
	# path('<int:product_id>/selection', views.selection, name='selection')
	path('<int:product_id>/<str:product_type>/selection', views.selection, name='selection'),
	path('client/', views.client_view, name='client'),
	path('client/purchasedone/', views.bill_view, name='genbill')
	# path('<int:pk>/success/', views)
]
