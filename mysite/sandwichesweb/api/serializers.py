from abc import ABC

from rest_framework import serializers

from ..models import *


class SelectionProductsSerializer(serializers.Serializer, ABC):
	product_id = serializers.IntegerField()
	product_type = serializers.CharField(max_length=20)
	decision = serializers.IntegerField()
