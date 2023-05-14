from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=50, null=True)
    
    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    choices = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, null=True, choices=choices)
    Tags = models.ManyToManyField(Tag)    
    
    def __str__(self) -> str:
        return self.name
    
class Order(models.Model):
    choices = (
        ('Pending','Pending'),
        ('Out for delevery', 'Out for delevery'),
        ('Deliverd', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, null=True, choices=choices)
    
    def __str__(self) -> str:
        return f"Customer: {self.customer} Product: {self.product}"