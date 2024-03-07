from django.db import models
from django.utils import timezone
from accounts.models import User

import datetime
# Create your models here.

class Todo(models.Model):
  def __str__(self):
      return self.title

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=50)
  text = models.TextField(max_length=500)
  due = models.DateTimeField()
  start = models.DateTimeField()

  def calculate_diff_due_now(self):
    now = timezone.now()
    diff = abs(self.due - now)
    time_units = ({"weeks": 1}, {"days": 1}, {"hours": 1}, {"minutes": 1})
    diff_list = [0] * 4  # [weeks, days, hours, minutes]
    for i, time_unit in enumerate(time_units):
      while(diff > timezone.timedelta(**time_unit)):
        diff_list[i] += 1
        diff -= timezone.timedelta(**time_unit)
    return diff_list


  def calculate_proportion(self):
    now = timezone.now()
    progress = now - self.start
    whole = self.due - self.start
    proportion = progress / whole
    return proportion
