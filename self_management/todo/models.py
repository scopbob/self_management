from django.db import models
from accounts.models import User

import datetime
# Create your models here.
class Category(models.Model):
    def __str__(self):
      return self.name

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    COLOR_CHOICES = {
      "#333333":"light_black",
      "#66ff66":"light_green",
      "#66ffff":"light_blue",
      "#3333cc":"deep_blue",
      "#ff0000":"red",
    }
    color = models.CharField(max_length=11, choices=COLOR_CHOICES, default="#66ffff")


class Todo(models.Model):
  def __str__(self):
      return self.title

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=50)
  text = models.TextField(max_length=500, blank=True)
  due = models.DateTimeField()
  start = models.DateTimeField()
  categorys = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
