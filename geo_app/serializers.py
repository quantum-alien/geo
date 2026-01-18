from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import GeoPoint, Message

class MessageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Message
        fields = ['id', 'user', 'point', 'content', 'created_at']
        read_only_fields = ['id', 'created_at', 'user']

class GeoPointSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    
    lat = serializers.SerializerMethodField()
    lon = serializers.SerializerMethodField()

    class Meta:
        model = GeoPoint
        fields = ['id', 'user', 'title', 'description', 'latitude', 'longitude', 'lat', 'lon', 'created_at']
        read_only_fields = ['id', 'created_at', 'user', 'lat', 'lon']

    def get_lat(self, obj):
        return obj.location.y

    def get_lon(self, obj):
        return obj.location.x

    def create(self, validated_data):
        lat = validated_data.pop('latitude')
        lon = validated_data.pop('longitude')
        location = Point(lon, lat, srid=4326) 
        
        return GeoPoint.objects.create(location=location, **validated_data)