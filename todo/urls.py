from django.urls import path
from . import views

app_name = "todo"
urlpatterns = [
  path("", views.IntroductionView.as_view(), name="introduction"),
  path("index/", views.IndexView.as_view(), name="index"),
  path("detail/<int:pk>/", views.DetailView.as_view(), name="detail"),
  path("create/", views.TaskCreateView.as_view(), name="create"),
  path("update/<int:pk>/", views.UpdateTask.as_view(), name="update"),
  path("delete/", views.DeleteCheck.as_view(), name="delete"),
  path("success/", views.SuccessCheck.as_view(), name="success"),
  path("category/", views.CategoryList.as_view(), name="category_index"),
  path("category/create", views.CreateCategory.as_view(), name="category_create"),
  path("category/update/<int:pk>/", views.UpdateCategory.as_view(), name="category_update"),
  path("category/delete/", views.DeleteCategoryCheck.as_view(), name="category_delete"),
  path("progress/", views.ProgressView.as_view(), name="progress"),
]
