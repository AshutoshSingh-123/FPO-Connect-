"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path
from . import views as product_view
from .views import product_fpo_del, product_fpo_update, fpo_update
urlpatterns = [
path('', views.store, name='store'),
path('register/', views.fpo_register, name='fpo_register'),
path('cart/', views.cart, name='cart'),
path('allfpo/', views.fpo_listview, name='fpo_list'),
path('fpo_view/<int:slug>/', views.fpo_view, name='fpo_view'),
path('view/<int:slug>/', views.viewpage, name='view'),
path('<int:slag>/detail/', views.detail, name='checkout'),
path('<int:slag>/', views.addtocart, name='addtocart'),
path('onview_page/<int:slag>/', views.addtocart_onview_page, name='addtocart1'),
path('<int:id>/delete/', views.delete_item, name='delete'),
path('delete_fpo_product/<int:pk>/', product_fpo_del.as_view(template_name='store/delete_fpo_product.html'), name='delete'),
path('update_fpo/<int:pk>/', fpo_update.as_view(template_name='store/update_fpo.html'), name='update_fpo'),
path('update_fpo_product/<int:pk>/', product_fpo_update.as_view(template_name='store/update_fpo_product.html'), name='delete'),
path('create/', product_view.createview.as_view(template_name='store/createproduct.html'),name='createview'),
]
