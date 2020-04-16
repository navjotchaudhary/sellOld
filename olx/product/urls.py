from django.urls import path 
from . import views 
app_name = "product"
urlpatterns = [

    path('',views.productList, name = 'product_list'),
    path('category/<slug:category_slug>',views.productList, name = 'category'),
    path('<slug:product_slug>',views.productDetail, name = 'product_detail'),
    path('add/',views.addProduct,name = 'addproduct')
    
]