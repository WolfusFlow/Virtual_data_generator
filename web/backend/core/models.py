from django.db import models

class Data(models.Model):
    server_name = models.CharField(max_length=60)
    date_type = models.CharField(max_length=40)
    value = models.IntegerField()
    created_at = models.DateField()