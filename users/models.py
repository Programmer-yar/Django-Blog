from django.db import models
from django.contrib.auth.models import User
from PIL import Image   #from pillow library import image

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE) #One to one relationship with(name of model)
	"""CASCADE means if we delete the the user then also delete the profile but not vice versa"""
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')


	def __str__(self):
		#Dipslays specific itmes with customization
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		#This method runs after our form is saved


		""" 'Positional' and "keyword" arguments (that are captured in url patterns)
	    are assigned to 'args' and "kwargs" respectively"""
		#First run the save method of our parent class
		super(Profile, self).save(*args, **kwargs)
		"""When you are overriding model's save method in Django,
		you should also pass *args(positional arguments) and **kwargs(keyword arguments) 
		to overridden method. """

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)  #tuple
			img.thumbnail(output_size)

			img.save(self.image.path)  #override the existing image in the same path








