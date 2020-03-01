from django.db import models
from django.contrib.auth.models import User
# from django.contrib.gis.db import models
# from django.contrib.gis.geos import Point
# from location_field.models.spatial import LocationField
# from location_field.models.plain import PlainLocationField
class Event(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField()
    description = models.TextField(max_length=255)
    #city = models.CharField(max_length=255)
    # location = LocationField(based_fields=['city'], zoom=7, default=Point(1.0, 1.0))
    #location = PlainLocationField(based_fields=['city'], zoom=7,)
    location = models.TextField()
    datetime = models.DateField()
    seats= models.PositiveIntegerField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    #Method to update the tickets number:
    def tickets_left(self):
        return self.seats-self.tickets_num

class Booking(models.Model):
    tickets_num=models.ForeignKey(Event, on_delete=models.CASCADE)
