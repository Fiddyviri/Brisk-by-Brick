from django.db import models
from django.conf import settings

# Create your models here.

class Task(models.Model):
    PRIORITY_CHOICES =[
        ('not_urgent', 'Not Urgent'),
        ('not_important', 'Not Important'),
        ('urgent', 'Urgent'),
        ('important', 'Important'),
        ('both', 'Both')
    ]
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_name =models.TextField()
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICES, default='Not Urgent')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_private = models.BooleanField(default=True)
    progress_media =models.FileField( upload_to='task/progress/', null=True, blank=True)
    updated_at =models.DateTimeField( auto_now=True)

    def __str__(self):
        return self.task_name

class Goal(models.Model):
    STATUS_CHOICES =[
        ('pending','Pending'),
        ('in_progress', 'In Progress'),
        ('on_hold','On Hold'),
        ('completed', 'Completed')]
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal_name =models.TextField()
    description = models.TextField(blank=True)
    measurement = models.TextField()
    reward = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    # completed = models.BooleanField(default=False)
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.goal_name

class Letter(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.TextField()
    content = models.TextField(blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

class Notification(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message =models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"

class ForumPost(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to="community/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)

    task = models.ForeignKey(Task, null=True, blank=True, on_delete=models.SET_NULL)
    # likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_fposts', blank=True)

    def __str__(self):
        return self.content

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()

class ForumComment(models.Model):
    fpost = models.ForeignKey(ForumPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")

    def __str__(self):
        return f'Comment by {self.user.username} - {self.fpost.content[:30]}'

class ForumLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fpost = models.ForeignKey(ForumPost, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'fpost') 