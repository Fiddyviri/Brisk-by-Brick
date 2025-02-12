from django.urls import path
from .views import HomePageView, AboutPageView, FaqPageView
# from briskbrick.views import Forum_list


urlpatterns = [
path("", HomePageView.as_view(), name="home"),
path("about/", AboutPageView.as_view(), name="about"),
path("faqs/", FaqPageView.as_view(), name="faqs"),
# path("community/", Forum_list, name="forum_list")
]