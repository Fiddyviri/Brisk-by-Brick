from django.conf import settings
from django.db import models
from django.urls import reverse
# Create your models here.


# class NewsletterForm(models.Model):
#     first_name = models.CharField(max_length=200)
#     email = models.EmailField()
#     phone = models.CharField( max_length=15, null=True, blank=True)

class Post(models.Model):
    title = models.CharField( max_length=500)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField()
    date = models.DateField(auto_now=False, auto_now_add=False)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    
    