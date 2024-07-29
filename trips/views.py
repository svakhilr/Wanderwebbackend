from rest_framework import viewsets
from .models import TripPackage,TripBooking
from .serializers import TripPackageRetrieveSerializer,TripaPackageListSerializer,TripBookingCreateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class TripPckageViewset(viewsets.ModelViewSet):
    queryset = TripPackage.objects.all()    
    serializer_classes = {
        'create':TripPackageRetrieveSerializer,
        'list':TripaPackageListSerializer,
        'retrieve':TripPackageRetrieveSerializer,
        'update':TripPackageRetrieveSerializer,
        'partial_update':TripPackageRetrieveSerializer
    }

    def get_serializer_class(self):
        return self.serializer_classes[self.action]
    

class TripBookingViewset(viewsets.ModelViewSet):
    queryset = TripBooking.objects.all()
    serializer_class = TripBookingCreateSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        customer = self.request.user.customer
        context.update({"customer":customer})
        return context

    
   