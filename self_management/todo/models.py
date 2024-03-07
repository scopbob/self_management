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

  def calculate_proportion(self):
    now = timezone.now()
    progress = now - self.start
    whole = self.due - self.start
    proportion = progress / whole
    return proportion
