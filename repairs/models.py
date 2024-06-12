from django.db import models

class repair(models.Model):
    vehicle = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    steps = models.JSONField()

    def __str__(self):
        return f'{self.vehicle} - {self.status}'