from django.db import models
from django.contrib.auth.models import User  

# Create your models here.

class UserProfile(models.Model):

    role_choices = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('staff', 'Staff'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
         related_name='profile'
         
    )
    role = models.CharField(
        max_length=10,
        choices=role_choices, 
        default='customer'
    )
    phone = models.CharField(
        max_length=10,
        blank=True,
        null=True
    )
    def __str__(self):
        return self.user.username
    