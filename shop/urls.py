from django.urls import path

app_name = 'shop'

from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='product_list'),
]
