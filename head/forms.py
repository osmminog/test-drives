from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, label="Ваше имя")
    email = forms.EmailField(label="Ваш e-mail")
    to = forms.EmailField(label="Кому e-mail")
    comments = forms.CharField(required=False, widget=forms.Textarea, label="Комментарии")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class SearchForm(forms.Form):
    query = forms.CharField()
