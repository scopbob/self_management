from django.db import models
from accounts.models import User


# Create your models here.
class Category(models.Model):
    def __str__(self):
      return self.name

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)


class Todo(models.Model):
  def __str__(self):
      return self.title

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=50)
  text = models.TextField(max_length=500, blank=True)
  due = models.DateTimeField()
  start = models.DateTimeField()
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

  PRIORITY_CHOICES = {
    1:"high",
    2:"middle",
    3:"low"
  }
  priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
