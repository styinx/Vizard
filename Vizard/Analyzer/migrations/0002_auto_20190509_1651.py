# Generated by Django 2.1.7 on 2019-05-09 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Analyzer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
