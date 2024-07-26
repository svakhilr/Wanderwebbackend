from django.db import models


class TripPackage(models.Model):
    PACKAGE_IMAGE = 'trips/banner'
   
    package_name = models.CharField(max_length=70)
    location = models.CharField(max_length=70,null=True)
    package_discription = models.TextField(blank=True,null=True)
    days = models.IntegerField(null=True)
    price_per_head = models.DecimalField(max_digits=10,decimal_places=2)
    package_banner_image = models.ImageField(upload_to=PACKAGE_IMAGE)
    package_inclusions = models.TextField()
    package_exclusions = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.package_name  


class TripExclusion(models.Model):
    trip = models.ForeignKey(TripPackage,on_delete=models.CASCADE,related_name='exclusion')
    exclusion = models.CharField(max_length=80)

    def __str__(self):
        return f"Exclusion-------{self.trip.package_name}"  
    
class TripInclusion(models.Model):
    trip = models.ForeignKey(TripPackage,on_delete=models.CASCADE,related_name='inclusion')
    inclusion = models.CharField(max_length=80)

    def __str__(self):
        return f"Inclusion-------{self.trip.package_name}"  
