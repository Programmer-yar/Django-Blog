from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
	""" As we do not want to create additional fields we will directly go to "class:Meta" """
	class Meta:
		model = Comment
		fields = ['comment']
			



