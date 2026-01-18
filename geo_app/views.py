from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D 
from .models import GeoPoint, Message
from .serializers import GeoPointSerializer, MessageSerializer

class PointViewSet(viewsets.ModelViewSet):
    queryset = GeoPoint.objects.all().order_by('-created_at')
    serializer_class = GeoPointSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CreateMessageView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PointSearchView(generics.ListAPIView):
    serializer_class = GeoPointSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lat = self.request.query_params.get('latitude')
        lon = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius') 

        if lat and lon and radius:
            user_location = Point(float(lon), float(lat), srid=4326)
            return GeoPoint.objects.filter(
                location__distance_lte=(user_location, D(km=float(radius)))
            )
        return GeoPoint.objects.none()

class MessageSearchView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        lat = self.request.query_params.get('latitude')
        lon = self.request.query_params.get('longitude')
        radius = self.request.query_params.get('radius')

        if lat and lon and radius:
            user_location = Point(float(lon), float(lat), srid=4326)
            return Message.objects.filter(
                point__location__distance_lte=(user_location, D(km=float(radius)))
            ).select_related('point', 'user')
        return Message.objects.none()