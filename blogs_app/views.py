from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.generic import ( 
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView 
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post, Comment
from .forms import CommentForm
from .modules import Search_Function
from .serializers import CommentSerializer




#Function based views
def home(request):
	context = { 'posts': post.objects.all() }

	#Third argument "context" is used to pass information to template
	return render(request, 'blogs_app/home.html', context)
	
#Class based Views
class PostListView(ListView):
	model = Post   #This variable stores what model to query in order to create the list
	template_name = 'blogs_app/home.html' #app_name/model_viewtype.html
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

class UserPostListView(ListView):
	model = Post   #This variable stores what model to query in order to create the list
	template_name = 'blogs_app/user_posts.html' 
	context_object_name = 'posts'  
	#ordering = ['-date_posted']  overriden by get_query_set
	paginate_by = 5

	"""Positional and keyword arguments (that are captured in url patterns)
	 are assigned to args and kwargs respectively"""
	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


#Multiple Inheritance is not possible for (Detail and Create) class based views
# Because both classes expect different template names
def PostDetail(request, pk):

	post = Post.objects.get(id=pk)
	current_logged_in_user = request.user
	comments_list = Comment.objects.filter(blog=post).order_by('-date_added')
	# comments_list = list(comments_list.values())
	post_likes = post.likes.count()
	post_num = pk

	if current_logged_in_user in post.likes.all():
		like_status = 'Unlike'
	else:
		like_status = 'Like'

	if request.method == 'GET':
		form = CommentForm()

	#The below if statement handles multiple forms seperatly
	# the like buttons and comment form
	if request.method == 'POST':
		
		if 'comment_button' in request.POST:

			form = CommentForm(request.POST)
			if form.is_valid():
				new_comment = form.save(commit=False)
				new_comment.commentator = current_logged_in_user
				new_comment.blog = post 
				new_comment.save()
				return redirect('post-detail', pk=post_num) 

	
	

	context = {'post':post, 'comments_list':comments_list, 'post_likes':post_likes,
			   'like_status':like_status, 'form':form } 

	return render(request, 'blogs_app/post_detail.html', context)

#The below class based view was replaced by "PostDetail" function based view 
class PostDetailView(DetailView):

	model = Post
	def get_context_data(self, **kwargs):

		# Call the base implementation first to get a context
		context = super().get_context_data(**kwargs)
		#Add all the comments for a certain post
		context['comments_list'] = Comment.objects.filter(blog=self.object)
		context['form'] = form
		return context

def SearchPostList(request):
	
	#It capture queries from url
	#(queries start with '?' in url e.g http://localhost:8000/search/?search=my+updated)
	search_string = request.GET.get('search')
	filtered_posts = Post.objects.filter(title__icontains=search_string)
	#filtered_posts = Search_Function(search_string, all_posts)
	context = { 'filtered_posts':filtered_posts, 'captured_string':search_string }
	return render(request, 'blogs_app/search_posts.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)
		"""above return command runs form valid method on our parent class, usually runs by default
		but we are running it after we set the post author """


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
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
	model = Post

	#it will redirect to homepage url after successfully deleting the post
	success_url = '/'  

	def test_func(self):
		""" 'UserPassesTestMixin' class requires this function to work """
		
		post = self.get_object()  #method to get the post to be updated

		if self.request.user == post.author:
			return True

		else:
			return False


def about(request):
	return render(request, 'blogs_app/about.html', {'title': 'about'})
