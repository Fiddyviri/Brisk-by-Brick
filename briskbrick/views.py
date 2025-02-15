from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import re
from django.contrib.auth import get_user_model
from .models import Task, Goal, ForumPost, Letter, ForumComment, ForumLike, Notification
from .forms import TaskForm, GoalForm, LetterForm, ForumPostForm, ForumCommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import logout
from django.core.mail import send_mail
from datetime import timedelta
from django.utils.timezone import now


# Create your views here.
User = get_user_model()
@login_required
def fyp(request):
    tasks = Task.objects.filter(user=request.user)
    goals = Goal.objects.filter(user=request.user)
    letters = Letter.objects.filter(user=request.user)

    content ={
        'user': request.user,
        'tasks' : tasks, 
        'goals' : goals, 
        'letters' : letters
        }
    return render(request,'briskbrick/fyp.html', content)

@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('briskbrick:fyp')
    else:
        form = TaskForm()
    return render(request, 'briskbrick/task_form.html', {'form': form})

@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('briskbrick:fyp')
    else:
        form = TaskForm(instance=task)
    return render(request, 'briskbrick/task_form.html', {'form': form})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
        return redirect('briskbrick:fyp')
    return render(request, 'briskbrick/task_confirm_delete.html', {'task': task})

def check_private_task():
    one_week_ago = now() - timedelta(days=7)
    tasks= Task.objects.filter(is_private=True, updated_at__lte=one_week_ago)

    for task in tasks:
        task.is_private = False
        task.save()

        embarrassing_letter = Letter.objects.filter(user=task.user, active=True)

        fpost= ForumPost.objects.create(
            user=task.user,
            content= f"**{task.user.username}'s Task is Now Public!**\n\n**Task:**{task.task_name}\n**Punishment:**{embarrassing_letter}",
            task=task
        )

        # in app notification
        Notification.objects.create(user=task.user, message=f"Yo, Got Embarassed!, {task.task_name} is now public and posted")

        send_email_notification(task.user.email, 
                                'Yo, Got Embarassed! Private Task is Now Public',
                                "Hi @{task.user.username},<p>Since you didn't update your task to complet or shared progress, it has been made public alongside the letter.</p>"
                                )

@login_required
def goal_create(request):
    if request.method == "POST":
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('briskbrick:fyp')
    else:
        form = GoalForm()
    return render(request, 'briskbrick/goal_form.html', {'form': form})

@login_required
def goal_update(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    if request.method == "POST":
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            return redirect('briskbrick:fyp')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'briskbrick/goal_form.html', {'form': form})

@login_required
def goal_delete(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    if request.method == "POST":
        goal.delete()
        return redirect('briskbrick:fyp')
    return render(request, 'briskbrick/goal_confirm_delete.html', {'goal': goal})


# Board
@login_required
def board(request):
    letters = Letter.objects.filter(user=request.user)

    content ={
        'user': request.user,
        'letters' : letters
    }
    return render(request,'briskbrick/board.html', content)
@login_required
def letter_create(request):
    if request.method == "POST":
        form = LetterForm(request.POST)
        if form.is_valid():
            letter = form.save(commit=False)
            letter.user = request.user
            letter.save()
            return redirect('briskbrick:board')
    else:
        form = LetterForm()
    return render(request, 'briskbrick/letter_form.html', {'form': form})


@login_required
def letter_delete(request, letter_id):
    letter = get_object_or_404(Letter, id=letter_id, user=request.user)
    if request.method == "POST":
        letter.delete()
        return redirect('briskbrick:board')
    return render(request, 'briskbrick/letter_confirm_delete.html', {'letter': letter})

def Forum_list(request):
    fposts = ForumPost.objects.all()
    return render(request,'briskbrick/community.html',{'fposts' : fposts})
    
def forum_post_detail(request, fpost_id):
    fpost = get_object_or_404(ForumPost, id=fpost_id)
    comments = ForumComment.objects.filter(fpost=fpost)
    liked = fpost.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
    return render(request, 'briskbrick/post_detail.html', {'fpost': fpost, "comments": comments, "liked": liked})

@login_required
def add_comment(request, fpost_id):
    fpost = get_object_or_404(ForumPost, id=fpost_id)
    if request.method == "POST":
        form = ForumCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Use request.user
            comment.fpost = fpost

            # Handle replies
            parent_id = request.POST.get("parent_id")
            if parent_id:
                parent_comment = ForumComment.objects.filter(id=parent_id).first()
                if parent_comment:
                    comment.parent = parent_comment

            comment.save()

            # Handle @ mentions
            
            mentioned_users = re.findall(r"@(\w+)", comment.content)  
            for username in mentioned_users:
                mentioned_user = User.objects.filter(username=username).first()
                if mentioned_user:
                    # Notify user (if needed, add a notification system)
                    #  Notification.objects.create(user=fpost.user, 
                    #             message=f"{User.username} commented on your post:{comment[:50]}")
                  pass  

                # Notification.objects.create(user=fpost.user, 
                #                 message=f"{User.username} commented on your post:{comment[:50]}")
            return redirect("briskbrick:post_detail", fpost_id=fpost.id)
    else:
        form = ForumCommentForm()
    
    return render(request, "briskbrick/add_comment.html", {"form": form, "fpost": fpost})

@login_required
def like_post(request, fpost_id):
    fpost = ForumPost.objects.get( id=fpost_id)
    like, created = ForumLike.objects.get_or_create(fpost=fpost, user=request.user)
    if not created:
        like.delete()  # Unlike if already liked

    Notification.objects.create(user=fpost.user, 
                                message=f"{User.username} liked your post")
    return redirect("briskbrick:post_detail", fpost_id=fpost.id)

@login_required
def create_forum_post(request):
    if request.method == "POST":
        form = ForumPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("briskbrick:forum_list")
    else:
        form = ForumPostForm()

    return render(request, "briskbrick/create_post.html", {"form": form})

@login_required
def edit_forum_post(request, fpost_id):
    fpost = get_object_or_404(ForumPost, id=fpost_id, user=request.user)  # Ensure only owner can edit
    if request.method == "POST":
        form = ForumPostForm(request.POST, instance=fpost)
        if form.is_valid():
            form.save()
            return redirect("briskbrick:post_detail", fpost_id=fpost.id)
    else:
        form = ForumPostForm(instance=fpost)
    
    return render(request, "briskbrick/edit_post.html", {"form": form, "fpost": fpost})

@login_required
def delete_forum_post(request, fpost_id):
    fpost = get_object_or_404(ForumPost, id=fpost_id, user=request.user)  # Only owner can delete
    if request.method == "POST":
        fpost.delete()
        return redirect("briskbrick:forum_list")
    
    return render(request, "briskbrick/delete_post_confirm.html", {"fpost": fpost})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(ForumComment, id=comment_id, user=request.user)  # Only owner can delete
    fpost_id = comment.fpost.id
    if request.method == "POST":
        comment.delete()
        return redirect("briskbrick:post_detail", fpost_id=fpost_id)

    return render(request, "briskbrick/delete_comment_confirm.html", {"comment": comment})

# profile
@login_required
def profile(request, username):
    # User = request.user
    user= User.objects.get(username=username)
    user_posts = ForumPost.objects.filter(user=user)
    return render(request, "briskbrick/profile.html",{'user': user, 'user_posts': user_posts, 'page-title': user.username})

@login_required
def settings(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("briskbrick:profile")  # Redirect back to profile
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, "briskbrick/settings.html", {"form": form})

@login_required
def user_logout(request):
    logout(request)
    return redirect("login") 
# Notifications
@login_required
def notification(request):
    notifications = Notification.objects.filter(user=request.user)

    content ={
        'user': request.user,
        'notifications' : notifications
    }
    return render(request,'briskbrick/notification.html', content)

def send_email_notification(user_email,subject, message):
    send_mail(

        subject,
        message,
        "abelefidelis@gmail.com",[user_email],
        fail_silently=False,
    )

def task_reminders():
    overdue_tasks = Task.objects.filter(reminder_date__lte=now(), completed=False)
    
    for task in overdue_tasks:
        send_email_notification(
            task.user.email,
            'Yo!, You just close to embarrass yourself',
            f" Hey @{task.user.username}, don't forget to complete : {task.task_name}! "
        )