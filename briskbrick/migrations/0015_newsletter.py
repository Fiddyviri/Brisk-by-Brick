# Generated by Django 5.1.5 on 2025-02-12 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('briskbrick', '0014_forumpost_task_letter_active_task_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
    ]
