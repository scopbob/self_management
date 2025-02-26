from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import Todo, Category


class TodoModelForm(forms.ModelForm):
  due = forms.SplitDateTimeField(widget=forms.widgets.SplitDateTimeWidget(date_attrs={"type":"date"}, time_attrs={"type":"time"}))
  start = forms.SplitDateTimeField(widget=forms.widgets.SplitDateTimeWidget(date_attrs={"type":"date"}, time_attrs={"type":"time"}))
  class Meta:
    model = Todo
    exclude = ["user"]

  def __init__(self, user=None, *args, **kwargs):
      self.user = user
      super().__init__(*args, **kwargs)
      self.fields["start"].initial = timezone.now().replace(second=0)
      for field in self.fields.values():
          field.widget.attrs['class'] = 'form-control'
          field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる

  def save(self, commit=True):
      todo = super().save(commit=False)
      if self.user:
          todo.user = self.user
      if commit:
          todo.save()
      return todo

  def clean(self):
    cleaned_data = super().clean()
    due = cleaned_data.get("due")
    start = cleaned_data.get("start")
    if due <= start:
      raise ValidationError("due must be set after start")


class CategoryModelForm(forms.ModelForm):
  color = forms.CharField(widget=forms.TextInput(attrs={'type': 'color'}))
  class Meta:
    model = Category
    exclude = ["user"]

  def __init__(self, user=None, *args, **kwargs):
      self.user = user
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
        field.widget.attrs['class'] = 'form-control'
        field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる

  def save(self, commit=True):
      todo = super().save(commit=False)
      if self.user:
          todo.user = self.user
      if commit:
          todo.save()
      return todo
