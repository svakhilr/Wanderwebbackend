from rest_framework import viewsets,status
from .models import TripPackage,TripBooking
from .serializers import (TripPackageRetrieveSerializer,
    TripaPackageListSerializer,TripBookingCreateSerializer,
    TripBookingListserailizer,CheckoutSerializer,SuccessPaymentSerializer)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.exceptions import ValidationError
import stripe

FRONTEND_CHECKOUT_SUCCESS_URL="http://localhost:3000/checkout-success/?session_id={CHECKOUT_SESSION_ID}"
FRONTEND_CHECKOUT_FAILED_URL="http://localhost:3000/checkout-failed"


stripe.api_key= settings.STRIPE_SECRET_KEY

class TripPckageViewset(viewsets.ModelViewSet):
    queryset = TripPackage.objects.all()    
    serializer_classes = {
        'create':TripPackageRetrieveSerializer,
        'list':TripaPackageListSerializer,
        'retrieve':TripPackageRetrieveSerializer,
        'update':TripPackageRetrieveSerializer,
        'partial_update':TripPackageRetrieveSerializer,
        
    }

    def get_serializer_class(self):
        return self.serializer_classes[self.action]
    

class TripBookingFilter(filters.FilterSet):
    booking_id = filters.CharFilter(method='filter_by_booking_id')

    def filter_by_booking_id(self,queryset,*args):
        booking_id = self.request.query_params.get("booking_id")
        return queryset.filter(booking_id=booking_id)
        


    class Meta:
        model=TripBooking
        fields =('booking_id',)

    

class TripBookingViewset(viewsets.ModelViewSet):
    queryset = TripBooking.objects.all()
    serializer_classes = {
        "list":TripBookingListserailizer,
        "retrieve":TripBookingCreateSerializer,
        "create":TripBookingCreateSerializer,
        "update":TripBookingCreateSerializer,
        "partial_update":TripBookingCreateSerializer,
        'checkout':CheckoutSerializer,
        "success_payment":SuccessPaymentSerializer
    } 
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TripBookingFilter

    def get_serializer_class(self):
        # if self.action in ["list","retrieve","create","update","partial_update"]:
        return self.serializer_classes[self.action]
        

    def get_serializer_context(self):
        context = super().get_serializer_context()
        customer = self.request.user.customer
        context.update({"customer":customer})
        return context
    
    def get_object(self):
        print(self.kwargs["pk"])
        # if self.kwargs["pk"] == "me":
        #     return TripBooking.objects.get(customer=self.request.user.customer)
        return super().get_object()
    
    def list(self, request, *args, **kwargs):
        print("listing")
        return super().list(request, *args, **kwargs)
    
    
    @action(methods=["post"], detail=False)
    def checkout(self,request,*args,**kwargs):
        amount = float(request.data["amount"])
        package_name = request.data["package_name"]
        booking_id = request.data["booking_id"]
        print("bookingprice",int(amount))
       
        # try:
        checkout_session = stripe.checkout.Session.create(
            line_items =[{
            'price_data' :{
            'currency' : 'usd',  
                'product_data': {
                'name': package_name,
                },
            'unit_amount': int(amount)*100
            },
            'quantity' : 1
        }],
            metadata={"booking_id": booking_id},
            mode= 'payment',
            success_url= FRONTEND_CHECKOUT_SUCCESS_URL,
            cancel_url= FRONTEND_CHECKOUT_FAILED_URL,
            )
        data = {
            "url":checkout_session.url
        }
        return Response(data,status=status.HTTP_200_OK)
            # return redirect(checkout_session.url ,code=303)
        # except Exception as e:
        #     print(e)
        # return e
    
    @action(methods=["post"], detail=False)
    def success_payment(self,request,*args,**kwargs):
        session_id = request.data["session_id"]
        session = stripe.checkout.Session.retrieve(session_id)
        booking_id = session.metadata.get('booking_id')

        try:
            booking_data = TripBooking.objects.get(booking_id=booking_id)
        except TripBooking.DoesNotExist:
            raise ValidationError("Booking Data Does Not Exist")
        booking_data.booking_status = booking_data.COMPLETED
        booking_data.payment_session_id = session_id
        booking_data.save()
        serializer = TripBookingListserailizer(booking_data)
        return Response(serializer.data,status=status.HTTP_200_OK)
        




    


    
    
   