from django.db import models
from .trip import TripPackage

class PackageItnary(models.Model):
    PACKAGE_IMAGE = 'trips/Itnary'
    
    package = models.ForeignKey(TripPackage,on_delete=models.CASCADE,related_name='itnary')
    title = models.CharField(max_length=20)
    image = models.ImageField(upload_to=PACKAGE_IMAGE)
    discription = models.TextField()
    
    def __str__(self):
        return f"{self.package.package_name} -------- {self.title}"