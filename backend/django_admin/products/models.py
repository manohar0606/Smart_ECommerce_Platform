from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    stock=models.PositiveIntegerField(default=0)
    category=models.CharField(max_length=100,default='General')
    is_active=models.BooleanField(default=True)
    image_url=models.URLField(max_length=200,blank=True,null=True)
    
    def __str__(self):
        return self.name