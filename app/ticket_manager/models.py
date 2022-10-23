from django.db import models
from django.contrib.auth.models import AbstractUser

class Status(models.Model):
  created_date = models.DateTimeField(auto_now = True)
  status = models.CharField(max_length=50)
  order = models.FloatField(verbose_name="上流からの番号")
  
  def __str__(self):
    return self.status

class Category(models.Model):
  created_date = models.DateTimeField(auto_now = True)
  category = models.CharField(max_length=50)
  
  def __str__(self):
    return self.category

class Ticket(models.Model):
  created_date = models.DateTimeField(auto_now = True)
  title = models.CharField(max_length = 200)
  description = models.CharField(max_length = 500)
  status = models.ForeignKey(Status, verbose_name="ステータス", on_delete=models.PROTECT, null = True)
  category = models.ForeignKey(Category, verbose_name="カテゴリ", on_delete=models.PROTECT, null = True)
  deadlinedate = models.DateTimeField(null=True, verbose_name='終了予定日')
  lastupdatedate = models.DateTimeField(auto_now=True, verbose_name='最終更新日')

class User(AbstractUser):
  pass

# Create your models here.
