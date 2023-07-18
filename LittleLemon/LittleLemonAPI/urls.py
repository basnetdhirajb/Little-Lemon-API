from django.urls import path
from . import views

urlpatterns = [
    path('menu-items',views.menu_items),
    path('menu-items/<str:menuItem>', views.each_menu_item),
]