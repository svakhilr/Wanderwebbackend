from django.db import models
from .trip import TripPackage
from customers.models import CustomerProfile
from django.utils.timezone import now



class TripBooking(models.Model):
    
    INITIATED = 'Initiated'
    COMPLETED = 'Completed'
    FAILED    = 'Failed'


    BOOKING_STATUS = (
        (INITIATED,'Initiated'),
        (COMPLETED,'Completed'),
        (FAILED,'Failed'))
    customer = models.ForeignKey(CustomerProfile,on_delete=models.CASCADE,related_name='tripbooking')
    trip_package = models.ForeignKey(TripPackage,models.CASCADE,related_name='tripbooking')
    booking_id = models.CharField(max_length=50,null=True,blank=True)
    booker_name = models.CharField(max_length=50)
    contact_number = models.CharField(max_length=10)
    booker_email = models.EmailField(null=True)
    total_participants = models.PositiveIntegerField()
    starting_date = models.DateField()
    ending_date = models.DateField()
    booking_status = models.CharField(max_length=20,choices=BOOKING_STATUS,default= INITIATED)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    booked_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.profile_name}--------{self.trip_package.package_name}"
    
    def save(self,*args,**kwargs):
        if not self.pk and not self.booking_id:
            super().save(*args,**kwargs)
            current_date = now().strftime('%Y%m%d')
            unique_id = f"IN{self.pk}{current_date}"
            self.booking_id = unique_id
            return self.save()
        print("ssavve")
        return super().save(*args,**kwargs)
