from django.contrib.gis.db import models
from django.contrib.auth.models import User

class GeoPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = models.PointField(srid=4326) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.location.x}, {self.location.y})"

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    point = models.ForeignKey(GeoPoint, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg by {self.user.username} on {self.point.title}"