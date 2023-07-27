from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('customers/', views.customers, name="customers"),
    path('customer/<str:pk>', views.customer, name="customer"),
    path('products/', views.products, name="products"),
    path('product_form/', views.product_form, name="product_form"),
    path('update_product/<str:pk>', views.update_product, name="update_product"),
    path('delete_product/<str:pk>', views.delete_product, name="delete_product"),
    path('orders/', views.orders, name="orders"),

    path('user/', views.user_page, name='user_page'),
    path('account/', views.accont_setting, name='account'),

    path('order_form/', views.order_form, name="order_form"),
    path('customer_orders/<str:pk>',
         views.customer_multiple_order_form, name="customer_orders"),
    path('update_order/<str:pk>', views.update_order, name="update_order"),
    path('delete_order/<str:pk>', views.delete_order, name="delete_order"),
    path('add_customer/', views.add_customer, name="add_customer"),
    path('update_customer/<str:pk>', views.update_customer, name="update_customer"),
    path('delete_customer/<str:pk>', views.delete_customer, name="delete_customer"),

    path('register/', views.register, name="register"),
    path('loginpage/', views.loginpage, name="loginpage"),
    path('logout/', views.logoutpage, name="logout"),

]
