from django.urls import path
from . import views

app_name = "todo"
urlpatterns = [
  path("", views.IndexView.as_view(), name="index"),
  path("detail/<int:pk>/", views.DetailView.as_view(), name="detail"),
  path("create/", views.CreateNewTask.as_view(), name="create"),
  path("update/<int:pk>/", views.UpdateTask.as_view(), name="update"),
  path("delete/", views.DeleteCheck.as_view(), name="delete"),
]
