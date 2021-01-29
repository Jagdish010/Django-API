from rest_framework import serializers
from ..models import UserProfile

class ProfileSerialize(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_name', 'age', 'gender', 'image', 'skill']