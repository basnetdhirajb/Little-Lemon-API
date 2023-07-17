from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import MenuItemSerializer
from .models import MenuItem
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view()
@permission_classes([IsAuthenticated])
def menu_items(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializer(items, many = True)
    return Response(serialized_item.data)