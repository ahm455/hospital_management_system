from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True)

        class Meta:
            model = User
            fields = ['id','username','password',
                      'email','phone','role','date_joined','date_of_birth']

        def create(self, validated_data):
            password = validated_data.pop("password")
            user = User(**validated_data)
            user.set_password(password)
            user.save()
            return user

class MiniUserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'username',"role"]


class DoctorSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = ["id", "user", "specialization"]


class PatientSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = ["id", "user"]



class NurseSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer(read_only=True)

    class Meta:
        model = Nurse
        fields = ["id", "user"]


class StaffSerializer(serializers.ModelSerializer):
    user = MiniUserSerializer(read_only=True)

    class Meta:
        model = Staff
        fields = ["id", "user"]