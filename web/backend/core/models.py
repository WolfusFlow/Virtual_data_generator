from django.db import models

class Data(models.Model):
    server_name = models.CharField(max_length=60)
    date_type = models.CharField(max_length=40)
    value = models.IntegerField()
    created_at = models.DateField()

    class Meta:
        ordering = ['server_name']

    def __str__(self):
        return f'Data from {self.server_name} is {self.value} at {self.created_at}'