from django.urls import path
from . import views

urlpatterns = [
    path('menu-items',views.menu_items),
    path('menu-items/<str:menuItem>', views.each_menu_item),
    path('groups/manager/users',views.ListUsers.as_view()),
    path('groups/manager/users/<int:userID>',views.ListUsers.as_view()),
    path('groups/delivery-crew/users', views.list_delivery_crew),
    path('groups/delivery-crew/users/<int:userID>', views.remove_delivery_crew),
    path('cart/menu-items', views.ManageCart.as_view({
        'get':'list',
        'post':'create',
        'delete':'destroy',
        })),
]