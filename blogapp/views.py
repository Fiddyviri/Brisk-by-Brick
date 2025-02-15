from django.shortcuts import render
from django.http import HttpResponseRedirect
# from .forms import NewsletterForm
from django.views.generic import ListView
from django.views.generic import DetailView
from .models import Post



# Create your views here.

# def newsletter(request):
#     if request.method == 'POST':
#         form = NewsletterForm(request.POST)
#         if form.is_valid():
#             subscribe = form.save(commit=False)
#             subscribe.save()
#             pass 
#     return render(request, 'blog.html', {'form': form})


class BlogListView(ListView):
    model = Post
    template_name = "blog.html"


class BlogDetailView(DetailView):
    model = Post
    template_name = "post_detail.html"


        
