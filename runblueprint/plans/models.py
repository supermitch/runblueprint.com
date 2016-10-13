from django.db import models

# class Runner(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     created_on = models.DateTimeField(auto_now_add=True)


class Plan(models.Model):
    s3URL = models.CharField(max_length=2000)
    created_on = models.DateTimeField(auto_now_add=True)
