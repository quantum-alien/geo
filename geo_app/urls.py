from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PointViewSet, CreateMessageView, PointSearchView, MessageSearchView

router = DefaultRouter()
router.register(r'points', PointViewSet, basename='points')

urlpatterns = [
    path('', include(router.urls)),
    
    path('points/messages/', CreateMessageView.as_view(), name='create-message'),
    
    path('points/search/', PointSearchView.as_view(), name='search-points'),
    
    path('messages/search/', MessageSearchView.as_view(), name='search-messages'),
]