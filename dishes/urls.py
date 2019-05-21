from django.contrib import admin
from django.urls import path
from dishes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('getCategory', views.getCategory, name='getCategory'),
    path('getType', views.getType, name='getType'),
    path('getPackage', views.getPackage, name='getPackage'),
    path('recommend', views.recommend, name='recommend'),
    path('submitOrder', views.submitOrder, name='submitOrder'),
    path('pickleMyHeaderTable', views.pickleMyHeaderTable, name='pickleMyHeaderTable'),
    path('search', views.search, name='searchDish'),
    path('deleteCookie', views.deleteCookie, name='deleteCookie'),
]