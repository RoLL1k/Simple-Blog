from django import forms
from .models import Tag, Post, Comment
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'short_description', 'body', 'tags']

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control w-50'}),
			'body': forms.Textarea(attrs={'class': 'form-control w-50'}),
			'short_description': forms.TextInput(attrs={'class': 'form-control w-75'}),
			'tags': forms.CheckboxSelectMultiple(),
		}


class TagForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = ['title']

		widgets = {
			'title': forms.TextInput(attrs={'class': 'form-control w-50'}),
		}


class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		exclude = ('date_pub',)
		widgets = {
			'author': forms.TextInput(attrs={'class': 'form-control w-50'}),
			'body': forms.Textarea(attrs={'class': 'form-control w-50'}),
			'post': forms.HiddenInput(),
			'comment': forms.HiddenInput(),
			}
