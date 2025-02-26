# Generated by Django 5.0.2 on 2024-03-09 07:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_category_todo_categorys'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='categorys',
        ),
        migrations.AlterField(
            model_name='todo',
            name='text',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='todo',
            name='categorys',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='todo.category'),
        ),
    ]
