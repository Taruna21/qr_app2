from django.db import models

# Create your models here.

class storeURL(models.Model):
    url = models.URLField()
    unique_id = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.url} - {self.unique_id}"