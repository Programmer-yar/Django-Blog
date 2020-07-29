from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ( 
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView 
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import post


#Function based views
def home(request):
	context = { 'posts': post.objects.all() }

	#Third argument "context" is used to pass information to template
	return render(request, 'blogs_app/home.html', context)
	#contextual meaning of 'render' is to return back	
	
#Class based Views
class PostListView(ListView):
	model = post   #This variable stores what model to query in order to create the list
	template_name = 'blogs_app/home.html' #app_name/model_viewtype.html
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

class UserPostListView(ListView):
	model = post   #This variable stores what model to query in order to create the list
	template_name = 'blogs_app/user_posts.html' 
	context_object_name = 'posts'
	#ordering = ['-date_posted']  overriden by get_query_set
	paginate_by = 5

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
	model = post


class PostCreateView(LoginRequiredMixin, CreateView):
	model = post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
		"""above return command runs form valid method on our parent class, usually runs by default
		but we are running it after we set the post author """


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


	def test_func(self):
		""" 'UserPassesTestMixin' class requires this function to work """
		post = self.get_object()  #method to get the post to be updated

		if self.request.user == post.author:
			return True

		else:
			return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = post
	success_url = '/'  #it will redirect to homepage url after successfully deleting the post

	def test_func(self):
		""" 'UserPassesTestMixin' class requires this function to work """
		
		post = self.get_object()  #method to get the post to be updated

		if self.request.user == post.author:
			return True

		else:
			return False


def about(request):
	return render(request, 'blogs_app/about.html', {'title': 'about'})
