from rest_framework import serializers
from .models import CustomerProfile
from users.models import CustomUser

class CustomerRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(source='user.password',write_only=True)
    confirm_password = serializers.CharField(source='user.confirm_password',write_only=True)

    class Meta:
        model = CustomerProfile
        fields = ('email','profile_name','password','confirm_password')

    def validate(self, attrs):
        print(attrs["user"]["password"])
        if attrs["user"]['password'] != attrs["user"]["confirm_password"]:
            raise serializers.ValidationError("password doesn't match")
        return super().validate(attrs)
    
    def create(self, validated_data):
        user = validated_data.pop("user")
        user = CustomUser.objects.create_user(email = user["email"],password=user["password"])
        validated_data["user"] = user
        return super().create(validated_data)
    



