from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Club,SocialAccount, Player, Match

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = "__all__"
        extra_kwargs = {'owner': {'read_only': True}}

class SocialAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAccount
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}



class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = "__all__"
