from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import MenuItemSerializer, CategorySerializer
from .models import MenuItem, Category
from rest_framework.permissions import IsAuthenticated

# Create your views here.
@api_view(['GET','POST','PATCH','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def menu_items(request):
    if request.method =='GET':
        items = MenuItem.objects.select_related('category').all()
        serialized_item = MenuItemSerializer(items, many = True)
        return Response(serialized_item.data, status.HTTP_200_OK)
    elif request.method == 'POST':
        if request.user.groups.filter(name='Manager').exists():
            serialized_item = MenuItemSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({'message':'OK'},status.HTTP_200_OK)
        else:
            return Response({'message':'Unauthorized'},status.HTTP_403_FORBIDDEN)
            
    else:
        return Response({'message':'Unauthorized'},status.HTTP_403_FORBIDDEN)

@api_view(['GET','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def each_menu_item(request, menuItem):
    
    if request.method == 'GET':
        item = get_object_or_404(MenuItem, title = menuItem)
        serialized_item = MenuItemSerializer(item, many = False)
        return Response(serialized_item.data, status.HTTP_200_OK)
    elif request.method == 'PUT':
        if request.user.groups.filter(name='Manager').exists():
            item = MenuItem.objects.get(title = menuItem)
            serialized_item = MenuItemSerializer(item,data=request.data)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({'message':'PUT Updated'}, status.HTTP_200_OK)
        else:
            return Response({'message':'Unauthorized'}, status.HTTP_403_FORBIDDEN)
    elif request.method == 'PATCH':
        if request.user.groups.filter(name='Manager').exists():
            item = MenuItem.objects.get(title = menuItem)
            serialized_item = MenuItemSerializer(item,data=request.data,partial = True)
            serialized_item.is_valid(raise_exception=True)
            serialized_item.save()
            return Response({'message':'Patch Updated'}, status.HTTP_200_OK)
        else:
            return Response({'message':'Unauthorized'}, status.HTTP_403_FORBIDDEN)   
    elif request.method == 'DELETE':
        if request.user.groups.filter(name='Manager').exists():
            item = MenuItem.objects.get(title = menuItem)
            item.delete()
            return Response({'message':'Deleted'}, status.HTTP_200_OK)
        else:
            return Response({'message':'Unauthorized'}, status.HTTP_403_FORBIDDEN)   