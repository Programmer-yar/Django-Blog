from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
	"""Class for making posts in the database"""
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)  #diff between auto_now and auto_add_now
	
	#One to many relationship between user and posts
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	#on_delete tells django to delete all posts of a deleted user
	#on_delete has other arguments as well
	likes = models.ManyToManyField(User, related_name='like')
	
	#Now we will use dunder(double underscore) str method to display post content in Queryset
	#These methods are also called "magic methods or special methods" detail available in 
	#Coreys object tutorials
	def __str__(self):
		"""Using this we can return how we want it to be printed"""
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})
		#reverse gives the full url as a string


class Comment(models.Model):
	""" Enables users to comment on posts """
	commentator = models.ForeignKey(User, on_delete=models.CASCADE)
	blog = models.ForeignKey(Post, on_delete=models.CASCADE)
	comment = models.CharField(max_length=200)
	date_added = models.DateTimeField(default=timezone.now)

	class meta:
		verbose_name_plural = 'comments'

	def __str__(self):
		return self.comment

