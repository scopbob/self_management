from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from .models import Todo
from .forms import TodoModelForm

# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
  template_name = "todo/index.html"

  def get_queryset(self):
    return Todo.objects.filter(user=self.request.user)

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["now"] = timezone.now()
    return context



class DetailView(LoginRequiredMixin, generic.DetailView):
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


class UpdateTask(LoginRequiredMixin, generic.edit.UpdateView):
  model = Todo
  template_name = "todo/update.html"
  form_class = TodoModelForm
  success_url = reverse_lazy("todo:index")
