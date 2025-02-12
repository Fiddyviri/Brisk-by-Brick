from django.urls import path
from . import views

app_name = 'briskbrick'


urlpatterns = [
    path("", views.fyp, name='fyp'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/update/<int:task_id>/', views.task_update, name='task_update'),
    path('tasks/delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('goals/create/', views.goal_create, name='goal_create'),
    path('goals/update/<int:goal_id>/', views.goal_update, name='goal_update'),
    path('goals/delete/<int:goal_id>/', views.goal_delete, name='goal_delete'),
    path("board/", views.board, name='board'),
    path('my-letter/create/', views.letter_create, name='letter_create'),
    path('my-letter/delete/<int:letter_id>/', views.letter_delete, name='letter_delete'),
    path("community/", views.Forum_list, name="forum_list"),
    path("community/create/", views.create_forum_post, name="create_post"),
    path('community/post/<int:fpost_id>/', views.forum_post_detail, name='post_detail'),
    path("community/post/<int:fpost_id>/comment/", views.add_comment, name="add_comment"),
    path("community/post/<int:fpost_id>/like/", views.like_post, name="like_post"),
    path("community/post/<int:fpost_id>/edit/", views.edit_forum_post, name="edit_forum_post"),
    path("community/post/<int:fpost_id>/delete/", views.delete_forum_post, name="delete_forum_post"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path("notification/", views.notification, name='notification'),
    path("<str:username>/", views.profile, name="profile"),
    path("settings/", views.settings, name="settings"),
    path("logout/", views.user_logout, name="logout"),
]