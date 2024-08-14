from rest_framework import serializers
from .models import CustomerProfile
from users.models import CustomUser

class CustomerRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(source='user.password',write_only=True)
    confirm_password = serializers.CharField(source='user.confirm_password',write_only=True)
    profile_pic = serializers.ImageField(read_only=True)
    class Meta:
        model = CustomerProfile
        fields = ('id','email','profile_name','profile_pic','password','confirm_password')

    def validate(self, attrs):
        print(attrs["user"]["password"])
        email = attrs["user"]["email"]
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email Already Exists")
        if attrs["user"]['password'] != attrs["user"]["confirm_password"]:
            raise serializers.ValidationError("password doesn't match")
        return super().validate(attrs)
    
    def create(self, validated_data):
        user = validated_data.pop("user")
        user = CustomUser.objects.create_user(email = user["email"],password=user["password"])
        validated_data["user"] = user
        return super().create(validated_data)
    

class CustomerProfileRetrieveSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    class Meta:
        model = CustomerProfile
        fields = ('profile_name','email','profile_pic')
    



