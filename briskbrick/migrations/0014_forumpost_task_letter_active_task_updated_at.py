# Generated by Django 5.1.5 on 2025-02-11 02:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('briskbrick', '0013_task_is_private_task_progress_media'),
    ]

    operations = [
        migrations.AddField(
            model_name='forumpost',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='briskbrick.task'),
        ),
        migrations.AddField(
            model_name='letter',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
