from users.models import CustomUser
from django.db import models


class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='customer')
    profile_name = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to='customer/profile',blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.profile_name