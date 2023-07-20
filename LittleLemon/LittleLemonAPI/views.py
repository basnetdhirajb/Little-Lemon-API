from django.shortcuts import render, get_object_or_404
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import *
from .models import MenuItem, Category
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from rest_framework import viewsets

# Using function based view
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
            return Response({'message':'OK'},status.HTTP_201_CREATED)
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
        

#Using class based view
        
class ListUsers(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    
    def get(self,request):
        users = User.objects.filter(groups__name='Manager')
        serialized_item = UserSerializer(users,many=True)
        return Response(serialized_item.data, status.HTTP_200_OK)
    
    def post(self, request):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username = username)
            managers = Group.objects.get(name = "Manager")
            managers.user_set.add(user)
            return Response({'message':'User Assigned to Manager'}, status.HTTP_201_CREATED)

    def delete(self, request, userID):
        user = get_object_or_404(User, id = userID)
        if user.groups.filter(name = 'Manager').exists():  #check if the user belongs to the manager group
            managers = Group.objects.get(name = "Manager")
            managers.user_set.remove(user)
            return  Response({'message':'User Removed from Manager'}, status.HTTP_200_OK)
        else:
            return Response({'message':'User is not part of the manager group'}, status.HTTP_200_OK)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated, permissions.IsAdminUser])
def list_delivery_crew(request):
    if request.method == 'GET':
        users = User.objects.filter(groups__name='Delivery Crew')
        serialized_item = UserSerializer(users, many = True)
        return Response(serialized_item.data, status.HTTP_200_OK)
    if request.method == 'POST':
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username = username)
            delivery_crew = Group.objects.get(name = 'Delivery Crew')
            delivery_crew.user_set.add(user)
            return Response({'message':'User added to delivery crew'}, status.HTTP_201_CREATED)
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, permissions.IsAdminUser])
def remove_delivery_crew(request, userID):
    user = get_object_or_404(User, id = userID)
    if user.groups.filter(name = 'Delivery Crew').exists():
        delivery_crew = Group.objects.get(name='Delivery Crew')
        delivery_crew.user_set.remove(user)
        return Response({'message':'User removed from Delivery Crew'}, status.HTTP_200_OK)
    else:
        return Response({'message':'User not part of delivery crew'}, status.HTTP_200_OK)
    
#using viewsets
class ManageCart(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    
    def list(self, request):
            user = request.user
            cart = Cart.objects.filter(user = user)
            serialized_item = CartSerializer(cart, many = True)
            return Response(serialized_item.data, status.HTTP_200_OK)
       
    def create(self, request):
        user = request.user
        menuItem = MenuItem.objects.get(title = request.data['menuItem'])
        quantity = request.data['quantity']
        unitPrice = menuItem.price
        data_to_pass = {
            'user_id' : user.id,
            'menuitem_id': menuItem.id,
            'quantity':quantity,
            'unit_price':unitPrice,
            'price':int(quantity)*int(unitPrice),
        }
        
        serialized_item = CartSerializer(data = data_to_pass)
        serialized_item.is_valid()
        serialized_item.save()
        return Response({'message':'Item added to the cart'}, status.HTTP_200_OK)
    
    def destroy(self, request):
        userID = request.user.id
        carts = Cart.objects.filter(user_id = userID)
        carts.delete()
        return Response({'message':'All Items removed from the cart'}, status.HTTP_200_OK)