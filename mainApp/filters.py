import django_filters
from . models import Product, Order, Customer

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name', 'category']
        
class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['customer', 'product', 'status']
        
class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'address']