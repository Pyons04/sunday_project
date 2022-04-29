from django.db import models

class Ticket(models.Model):
  created_date = models.DateField()
  title = models.CharField(max_length = 200)
  description = models.CharField(max_length = 500)

# Create your models here.
