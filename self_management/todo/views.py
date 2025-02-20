from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Todo, Category
from .forms import TodoModelForm, CategoryModelForm

class TodoCreaterOnly(UserPassesTestMixin):
  def test_func(self):
    user = self.request.user
    todo_pk = self.kwargs["pk"]
    creater = Todo.objects.get(pk=todo_pk).user
    return user.pk == creater.pk

  def handle_no_permission(self):
    return redirect("todo:index")

class CategoryCreaterOnly(UserPassesTestMixin):
  def test_func(self):
    user = self.request.user
    category_pk = self.kwargs["pk"]
    creater = Category.objects.get(pk=category_pk).user
    return user.pk == creater.pk

  def handle_no_permission(self):
    return redirect("todo:index")


class IndexView(LoginRequiredMixin, generic.ListView):
  template_name = "todo/index.html"

  def get_queryset(self):
    user_todo = Todo.objects.filter(user=self.request.user)
    if "category" in self.request.GET:
      filter = self.request.GET.get("category")
      if filter != "None":
        user_todo = user_todo.filter(category__name=filter)
    if "order" in self.request.GET:
      order = self.request.GET.get("order")
      if order != "None":
        user_todo = user_todo.order_by(order)
    return user_todo

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["category_list"] = Category.objects.filter(user=self.request.user)
    context["selected_category"] = self.request.GET.get("category")
    context["selected_order"] = self.request.GET.get("order")
    return context


class DeleteCheck(LoginRequiredMixin, generic.ListView):
  template_name = "todo/delete_list.html"

  def get_queryset(self):
    print(self.request.GET)
    if "delete" in self.request.GET:
      delete_check_list = self.request.GET.getlist("delete")
      return Todo.objects.filter(pk__in=delete_check_list, user=self.request.user)

  def post(self, request):
    post_pks = request.POST.getlist("delete")
    Todo.objects.filter(pk__in=post_pks, user=self.request.user).delete()
    return redirect("todo:index")


class DetailView(LoginRequiredMixin, TodoCreaterOnly, generic.DetailView):
  model = Todo
  template_name = "todo/detail.html"


class TaskCreateView(LoginRequiredMixin, generic.edit.CreateView):
  template_name = "todo/create.html"
  form_class = TodoModelForm
  success_url = reverse_lazy("todo:index")

  def get_form_kwargs(self):
    kwgs = super().get_form_kwargs()
    kwgs["user"] = self.request.user
    return kwgs


class UpdateTask(LoginRequiredMixin, TodoCreaterOnly, generic.edit.UpdateView):
  model = Todo
  template_name = "todo/update.html"
  form_class = TodoModelForm
  success_url = reverse_lazy("todo:index")


class CategoryList(LoginRequiredMixin, generic.ListView):
  template_name = "todo/category_index.html"

  def get_queryset(self):
    return Category.objects.filter(user=self.request.user)


class CreateCategory(LoginRequiredMixin, generic.edit.CreateView):
  template_name = "todo/category_create.html"
  form_class = CategoryModelForm
  success_url = reverse_lazy("todo:create")

  def get_form_kwargs(self):
    kwgs = super().get_form_kwargs()
    kwgs["user"] = self.request.user
    return kwgs

class UpdateCategory(LoginRequiredMixin, CategoryCreaterOnly, generic.edit.UpdateView):
  model = Category
  template_name = "todo/category_update.html"
  form_class = CategoryModelForm
  success_url = reverse_lazy("todo:category")
