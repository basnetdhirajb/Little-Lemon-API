from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category']