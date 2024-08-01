from rest_framework import viewsets
from .models import TripPackage,TripBooking
from .serializers import TripPackageRetrieveSerializer,TripaPackageListSerializer,TripBookingCreateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
 


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
    serializer_class = TripBookingCreateSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TripBookingFilter

    def get_serializer_context(self):
        context = super().get_serializer_context()
        customer = self.request.user.customer
        context.update({"customer":customer})
        return context
    
    def get_object(self):
        print(self.kwargs["pk"])
        if self.kwargs["pk"] == "me":
            return TripBooking.objects.get(customer=self.request.user.customer)
        return super().get_object()
    
    def list(self, request, *args, **kwargs):
        print("listing")
        return super().list(request, *args, **kwargs)

    
   