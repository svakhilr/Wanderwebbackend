from rest_framework import viewsets,status
from rest_framework.response import Response
from .serializers import CustomerRegisterSerializer
from trips.serializers import TripBookingListserailizer
from .models import CustomerProfile
from users.models import CustomUser
from rest_framework.permissions import IsAuthenticated,AllowAny
from config.smtp import send_otp
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist
from config.tokens import get_tokens_for_user
from trips.models import TripBooking
import datetime

class CustomerViewset(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerRegisterSerializer

    def get_permissions(self):
        if self.action in ['list','retrieve','update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes=[AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_object(self):
        if self.kwargs["pk"] == "me":
            return CustomerProfile.objects.get(user=self.request.user)
        return super().get_object()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        mail = instance.user.email
    
        try:
            send_otp(mail,instance.user)
        except:
            print("email sent error")
            
        
        return  Response({"message":"OTP send"},status=status.HTTP_201_CREATED)
        
    @action(detail=False, methods=["post"])    
    def verify_otp(self,request):
        email = request.data["email"]
        otp = request.data["otp"]
        print(otp)
        try:
            user = CustomUser.objects.get(email=email)
            print(otp, user.otp)
        except ObjectDoesNotExist:
            return Response({"message":"User not found"},status=status.HTTP_404_NOT_FOUND)
        print(type(otp))
        if int(otp) == user.otp:
            difference = user.otp_added_time.replace(tzinfo=None) - datetime.datetime.now()
            print(difference.total_seconds())
            if difference.total_seconds() < -180:
                return Response({"message":"Otp Expired!"},status=status.HTTP_400_BAD_REQUEST)
            user.is_verified = True
            user.save()
            tokens = get_tokens_for_user(user)
            profile_name = user.customer.profile_name
            profile_data = {
                "profile_name":profile_name
            }
            tokens.update(profile_data)
            return Response(tokens,status=status.HTTP_200_OK)

        
        return Response({"message":"otp does not match"},status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"])
    def login(self,request): 
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user =  CustomUser.objects.get(email=email)
        except:
            return Response({"message":"Incorrect Email"},status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return Response({"message":"Incorrect Password"},status=status.HTTP_404_NOT_FOUND)
        else:
            if not user.is_verified:
                return Response({"message":"User not verified"},status=status.HTTP_403_FORBIDDEN)
            tokens = get_tokens_for_user(user)
            profile_name = user.customer.profile_name
            profile_data = {
                "profile_name":profile_name
            }
            tokens.update(profile_data)
            return Response(tokens,status=status.HTTP_200_OK)
        
    @action(detail=True, methods=["get"])
    def get_trip_booking(self,request,*args,**kwargs):
        if kwargs['pk'] == 'me':
            customer = self.get_object()
        trips = TripBooking.objects.filter(customer=customer).order_by('-booked_date')
        serializer = TripBookingListserailizer(trips , many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)  
 
        

