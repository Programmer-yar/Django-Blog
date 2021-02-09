from django.urls import path
from .views import ( 
	PostListView, PostDetailView,
	PostCreateView, PostUpdateView,
	PostDeleteView, UserPostListView,
    PostDetail, #SearchPostListView
)
from . import views
from .api import api_like, api_comment

urlpatterns = [
    #first argument of path should be left empty for home page
    #In second argument call the function from views for that page
    #In third argument specify the name of url pattern

    #previous path using function based views " path('', views.home, name="blog-home") "

    #below path will look for template using formula "app_name/model_viewtype.html", Goto views.py to change this
    path('', PostListView.as_view(), name="blog-home"),
    path('user/<str:username>/', UserPostListView.as_view(), name="user-posts"),

    #"pk=primary key" PostDetailView expects "pk" variable 
    path('post/<int:pk>/', views.PostDetail, name="post-detail"),
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),


    #below url will open at "localhost:8000/blog/about"
    path('about/', views.about, name="blog-about"),

    #API
    path('api/like', api_like, name="api_like"),
    path('api/comment', api_comment, name="api_comment"),

    #Search URL this url will capture the variable search paased through template
    #and then passes it to view function
    path('search/', views.SearchPostList ,name="post-search"), 
]
