from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework import mixins
from rest_framework import generics

from ..models import *
from .serializers import *
from ..views import *


class SelectionProductsSerializer(APIView):
	def get(self, request, product_id, product_type, decision):
		selection(product_id)
		
		if decision == 2:
			return


