from django import forms
from .models import Task, Goal, Letter, ForumPost,ForumComment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_name', 'priority', 'completed', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'datetime-local'}),
        }

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['goal_name', 'description', 'measurement', 'reward', 'status', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'datetime-local'}),
        }

class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ['subject', 'content', 'delivery_date' ]
        widgets = {
            'delivery_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['content', 'image', 'is_anonymous']

class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ["content"]
    
    parent_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)  # For replies
