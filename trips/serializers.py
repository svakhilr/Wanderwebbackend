from .models import TripPackage,PackageItnary,TripInclusion,TripExclusion
from rest_framework import serializers


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