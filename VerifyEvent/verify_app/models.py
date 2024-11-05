from django.db import models

class Participant(models.Model):
    code = models.CharField(max_length=10, unique=True) 
    name = models.CharField(max_length=100)  
    company = models.CharField(max_length=100)
    status = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.name} ({self.company}) - Verified: {'Yes' if self.status else 'No'}"
