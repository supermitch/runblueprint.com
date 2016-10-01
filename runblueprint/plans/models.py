from django.db import models


Class Profile(models.Model):
    name = models.CharField(max_length=50)
    race_distance = models.IntegerField()

# Class Plan(models.Model):
# TODO how do we persist a plan? Maybe just regenerate it from the profile.
