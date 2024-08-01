from .models import TripPackage,PackageItnary,TripInclusion,TripExclusion,TripBooking
from rest_framework import serializers
from datetime import timedelta


class TripInclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model= TripInclusion
        fields = ('id','inclusion')

class TripExclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripExclusion
        fields = ('id','exclusion')


class PackageItnarySerializer(serializers.ModelSerializer):

    class Meta:
        model= PackageItnary
        fields = ('id','title','image','discription')

class TripPackageRetrieveSerializer(serializers.ModelSerializer):
    itnary = PackageItnarySerializer(many=True)
    inclusion = TripInclusionSerializer(many=True)
    exclusion = TripExclusionSerializer(many=True)
    class Meta:
        model = TripPackage
        fields = ('id','package_name','package_discription','location','days',
            'price_per_head','package_banner_image','inclusion',
            'exclusion','itnary')
        
class TripaPackageListSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripPackage
        fields = ('id','package_name','package_discription','location','days',
            'price_per_head','package_banner_image','package_inclusions',
            'package_exclusions')
        

class TripBookingCreateSerializer(serializers.ModelSerializer):
    package_id = serializers.IntegerField(write_only=True)
    booking_id = serializers.CharField(read_only=True)
    class Meta:
        model = TripBooking
        fields = ('id','booker_name','booker_email','booking_id','package_id','contact_number','total_participants','starting_date')

    def create(self, validated_data):
        package_id = validated_data.pop("package_id")
        trip_package = TripPackage.objects.get(id=package_id)
        ending_date =  validated_data["starting_date"]+ timedelta(days = trip_package.days-1)
        customer = self.context.get("customer")
        print("cus",customer)
        additional_data = {
            "customer":customer,
            "ending_date":ending_date,
            "trip_package":trip_package
        }
        validated_data.update(additional_data)
        bookingData = TripBooking.objects.create(**validated_data)
        print(validated_data["starting_date"]+timedelta(days=10))
        return bookingData