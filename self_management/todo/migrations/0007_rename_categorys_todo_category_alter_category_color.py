# Generated by Django 5.0.2 on 2024-03-09 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0006_alter_category_color'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='categorys',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='category',
            name='color',
            field=models.CharField(choices=[('#333333', 'light_black'), ('#66ff66', 'light_green'), ('#66ffff', 'light_blue'), ('#3333cc', 'deep_blue'), ('#ff0000', 'red')], default='#66ffff', max_length=11),
        ),
    ]