from django.db import models


class Runner(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)


class Plan(models.Model):
    runner = models.ForeignKey(Runner, on_delete=models.CASCADE)
    s3URL = models.CharField()
    created_on = models.DateTimeField(auto_now_add=True)
