from django.shortcuts import redirect
from django.views import generic
from django.utils.http import urlencode
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Todo, Category
from .forms import TodoModelForm, CategoryModelForm

class CreaterOnly(UserPassesTestMixin):
  def test_func(self):
    user = self.request.user
    todo_pk = self.kwargs["pk"]
    creater = Todo.objects.get(pk=todo_pk).user
    return user.pk == creater.pk

  def handle_no_permission(self):
    return redirect("todo:index")

def get_request_list(self, key):
  request_list = eval(self.request.GET.get(key))
  request_list = list(map(int, request_list))
  return request_list

def add_queryparam(redirect_name, parameters):
  redirect_url = reverse(redirect_name)
  add_parameters = urlencode(parameters)
  url = f'{redirect_url}?{add_parameters}'
  return url


class IndexView(LoginRequiredMixin, generic.ListView):
  template_name = "todo/index.html"

  def get_queryset(self):
    user_todo = Todo.objects.filter(user=self.request.user)
    if "category" in self.request.GET:
      filter = self.request.GET.get("category")
      return user_todo.filter(category__name=filter)
    return user_todo

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["category_list"] = Category.objects.filter(user=self.request.user)
      return context

  def post(self, request):
    if "delete" in request.POST:
      post_pks = request.POST.getlist("delete")
      if len(post_pks) == 0:
        messages.error(self.request, "選択されていません")
        return redirect("todo:index")
      url = add_queryparam("todo:delete", dict(delete_list=post_pks))
      return redirect(url)

    if "category" in request.POST:
      filter_element = request.POST.get("category")
      url = add_queryparam("todo:index", dict(category=filter_element))
      if filter_element == "no filter":
        return redirect("todo:index")
      return redirect(url)


class DeleteCheck(LoginRequiredMixin, generic.ListView):
  template_name = "todo/delete_list.html"

  def get_queryset(self):
    if "delete_list" in self.request.GET:
      delete_check_list = get_request_list(self, "delete_list")
      return Todo.objects.filter(pk__in=delete_check_list, user=self.request.user)

  def post(self, request):
    post_pks = request.POST.getlist("delete")
    Todo.objects.filter(pk__in=post_pks, user=self.request.user).delete()
    return redirect("todo:index")


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
