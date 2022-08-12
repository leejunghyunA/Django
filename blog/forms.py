# comment form 구현
from .models import Comment
from django import froms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'author', 'created_at', 'modified_at',)