from django.shortcuts import redirect
from django.views import generic
from django.utils.http import urlencode
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Todo
from .forms import TodoModelForm

class CreaterOnly(UserPassesTestMixin):
  def test_func(self):
    user = self.request.user
    todo_pk = self.kwargs["pk"]
    creater = Todo.objects.get(pk=todo_pk).user
    return user.pk == creater.pk

  def handle_no_permission(self):
    return redirect("todo:index")


class IndexView(LoginRequiredMixin, generic.ListView):
  template_name = "todo/index.html"

  def get_queryset(self):
    return Todo.objects.filter(user=self.request.user)

  def post(self, request):
    post_pks = request.POST.getlist("delete")
    if len(post_pks) == 0:
      messages.error(self.request, "選択されていません")
      return redirect("todo:index")
    redirect_url = reverse('todo:delete')
    parameters = urlencode(dict(delete_list=post_pks))
    url = f'{redirect_url}?{parameters}'
    return redirect(url)


class DeleteCheck(LoginRequiredMixin, generic.ListView):
  template_name = "todo/delete_list.html"

  def get_queryset(self):
    if "delete_list" in self.request.GET:
      delete_check_list = eval(self.request.GET.get("delete_list"))
      delete_check_list = list(map(int, delete_check_list))
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
