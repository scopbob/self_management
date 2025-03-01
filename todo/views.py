from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone

from .models import Todo, Category, Progress
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


class IntroductionView(generic.TemplateView):
    template_name = "todo/introduction.html"


class IndexView(LoginRequiredMixin, generic.ListView):
  template_name = "todo/index.html"

  def get_queryset(self):
    user_todos = Todo.objects.filter(user=self.request.user)
    if "category_filter" in self.request.GET:
      filter = self.request.GET.get("category_filter")
      if filter != "None":
        user_todos = user_todos.filter(category__name=filter)
    if "deadline_filter" in self.request.GET:
      filter = self.request.GET.get("deadline_filter")
      if filter == "within":
        user_todos = user_todos.filter(due__gte=timezone.now())
      if filter == "out":
        user_todos = user_todos.filter(due__lt=timezone.now())
    if "order" in self.request.GET:
      order = self.request.GET.get("order")
      if order != "None":
        user_todos = user_todos.order_by(order)
    return user_todos

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["category_list"] = Category.objects.filter(user=self.request.user)
    context["selected_category"] = self.request.GET.get("category_filter")
    context["selected_deadline"] = self.request.GET.get("deadline_filter")
    context["selected_order"] = self.request.GET.get("order")
    return context


class DeleteCheck(LoginRequiredMixin, generic.ListView):
  template_name = "todo/delete_list.html"

  def get_queryset(self):
    if "checked" in self.request.GET:
      delete_check_list = self.request.GET.getlist("checked")
      return Todo.objects.filter(pk__in=delete_check_list, user=self.request.user)

  def post(self, request):
    post_pks = request.POST.getlist("checked")
    Todo.objects.filter(pk__in=post_pks, user=self.request.user).delete()
    return redirect("todo:index")


class SuccessCheck(LoginRequiredMixin, generic.ListView):
  template_name = "todo/success_list.html"

  def get_queryset(self):
    if "checked" in self.request.GET:
      delete_check_list = self.request.GET.getlist("checked")
      return Todo.objects.filter(pk__in=delete_check_list, user=self.request.user)

  def post(self, request):
    post_pks = request.POST.getlist("checked")
    success_todos = Todo.objects.filter(pk__in=post_pks, user=request.user)

    #success + 1をするところ
    progress = Progress.objects.get(user=request.user)
    for todo in success_todos:
      start = todo.start
      due = todo.due
      remaining_proportion = (timezone.now()-start) / (due-start) *100
      if remaining_proportion > 100:
        progress.out_due_num = F("out_due_num") + 1
      elif remaining_proportion > 80:
        progress.within_due_lte100_num = F("within_due_lte100_num") + 1
      elif remaining_proportion > 60:
        progress.within_due_lte80_num = F("within_due_lte80_num") + 1
      elif remaining_proportion > 40:
        progress.within_due_lte60_num = F("within_due_lte60_num") + 1
      elif remaining_proportion > 20:
        progress.within_due_lte40_num = F("within_due_lte40_num") + 1
      elif remaining_proportion > 0:
        progress.within_due_lte20_num = F("within_due_lte20_num") + 1
    progress.save()
    success_todos.delete()
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

  def get_form_kwargs(self):
    kwgs = super().get_form_kwargs()
    kwgs["user"] = self.request.user
    return kwgs



class CategoryList(LoginRequiredMixin, generic.ListView):
  template_name = "todo/category_index.html"

  def get_queryset(self):
    return Category.objects.filter(user=self.request.user)


class CreateCategory(LoginRequiredMixin, generic.edit.CreateView):
  template_name = "todo/category_create.html"
  form_class = CategoryModelForm
  success_url = reverse_lazy("todo:category_index")

  def get_form_kwargs(self):
    kwgs = super().get_form_kwargs()
    kwgs["user"] = self.request.user
    return kwgs

class UpdateCategory(LoginRequiredMixin, CategoryCreaterOnly, generic.edit.UpdateView):
  model = Category
  template_name = "todo/category_update.html"
  form_class = CategoryModelForm
  success_url = reverse_lazy("todo:category")


class DeleteCategoryCheck(LoginRequiredMixin, generic.ListView):
  template_name = "todo/category_delete_list.html"

  def get_queryset(self):
    if "checked" in self.request.GET:
      delete_check_list = self.request.GET.getlist("checked")
      return Category.objects.filter(pk__in=delete_check_list, user=self.request.user)

  def post(self, request):
    post_pks = request.POST.getlist("checked")
    Category.objects.filter(pk__in=post_pks, user=self.request.user).delete()
    return redirect("todo:category_index")


class ProgressView(LoginRequiredMixin, generic.DetailView):
  template_name = "todo/progress.html"

  def get_object(self):
    user_progress = Progress.objects.get(user=self.request.user)
    return user_progress


  def get_total_success_num(self, progress):
    total = 0
    for k, v in progress.__dict__.items():
      if "due" in k:
        total += v
    return total


  def get_total_within_num(self, progress):
    total = 0
    for k, v in progress.__dict__.items():
      if "within" in k:
        total += v
    return total


  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["total_num"] = self.get_total_success_num(context["progress"])
    context["total_within_num"] = self.get_total_within_num(context["progress"])
    return context
