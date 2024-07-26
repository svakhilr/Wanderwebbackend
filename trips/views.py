from rest_framework import viewsets
from .models import TripPackage
from .serializers import TripPackageRetrieveSerializer,TripaPackageListSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


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
    
   