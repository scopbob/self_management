from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Todo
from .forms import TodoModelForm

class CreaterOnly(UserPassesTestMixin):
  def test_func(self):
    user = self.request.user
    todo_pk = self.kwargs["pk"]
    creater = Todo.objects.get(pk=todo_pk).user
    return user == creater

  def handle_no_permission(self):
    return redirect(reverse_lazy("todo:index"))


class IndexView(LoginRequiredMixin, generic.ListView):
  template_name = "todo/index.html"

  def get_queryset(self):
    return Todo.objects.filter(user=self.request.user)


class DetailView(LoginRequiredMixin, CreaterOnly, generic.DetailView):
  model = Todo
  template_name = "todo/detail.html"


class CreateNewTask(LoginRequiredMixin, generic.edit.CreateView):
  template_name = "todo/create.html"
  form_class = TodoModelForm
  success_url = reverse_lazy("todo:index")

  def get_form_kwargs(self):
    kwgs = super().get_form_kwargs()
    kwgs["user"] = self.request.user
    return kwgs


class UpdateTask(LoginRequiredMixin, CreaterOnly, generic.edit.UpdateView):
  model = Todo
  template_name = "todo/update.html"
  form_class = TodoModelForm
  success_url = reverse_lazy("todo:index")
