from django.db import models

class Status(models.Model):
  created_date = models.DateTimeField(auto_now = True)
  status = models.CharField(max_length=50)
  order = models.FloatField(verbose_name="上流からの番号")
  
  def __str__(self):
    return self.status

class Ticket(models.Model):
  created_date = models.DateTimeField(auto_now = True)
  title = models.CharField(max_length = 200)
  description = models.CharField(max_length = 500)
  status = models.ForeignKey(Status, verbose_name="ステータス", on_delete=models.PROTECT, null = True)

# Create your models here.
