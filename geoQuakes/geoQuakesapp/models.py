from django.db import models

class Quake(models.Model):
    Date = models.CharField(max_length=100)
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    Type = models.CharField(max_length=100)
    Depth = models.FloatField()
    Magnitude = models.FloatField()
    Magnitude_Type = models.CharField(max_length=100)
    ID = models.CharField(max_length=100)

    def __str__(self):
        return self.ID

    class Meta:
        verbose_name_plural = 'Quake'

class QuakePredictions(models.Model):
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    Magnitude = models.FloatField()
    Depth = models.FloatField()
    Score = models.FloatField()

    class Meta:
        verbose_name_plural = "Quake_Predictions"
