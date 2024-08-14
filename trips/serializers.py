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
        total_amount = validated_data["total_participants"]*trip_package.price_per_head
        customer = self.context.get("customer")
        print("totalamo",total_amount)
        additional_data = {
            "customer":customer,
            "ending_date":ending_date,
            "trip_package":trip_package,
            "total_amount":total_amount
        }
        validated_data.update(additional_data)
        bookingData = TripBooking.objects.create(**validated_data)
        print(validated_data["starting_date"]+timedelta(days=10))
        return bookingData
    

class TripBookingListserailizer(serializers.ModelSerializer):
    package_name = serializers.CharField(source='trip_package.package_name')
    location = serializers.CharField(source='trip_package.package_name')
    days = serializers.CharField(source='trip_package.days')
    price_per_head = serializers.CharField(source ='trip_package.price_per_head')
    
    class Meta:
        model = TripBooking
        fields = ('id','booker_name','booking_status','package_name','location','days','price_per_head','booker_email','booking_id',
        'contact_number','total_participants','total_amount','starting_date','ending_date')


class CheckoutSerializer(serializers.Serializer):
    booking_id = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10,decimal_places=2)
    package_name = serializers.CharField()

class SuccessPaymentSerializer(serializers.Serializer):
    session_id = serializers.CharField()