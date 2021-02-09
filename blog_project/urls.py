
from django.contrib import admin
from django.urls import path, include
from users import views as users_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

""" Whenever we type in a url in address bar like "localhost:8000/blog/" django ignores 
"localhost:8000" and looks for "blog/" in urls.py in project folder. If a match is found
it checks to see where it should direct people who entered that address """

urlpatterns = [

    path('admin/', admin.site.urls),
    path('register/', users_view.register, name="register"),
    path('profile/', users_view.profile, name="profile"),

    #built in views
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name="password_reset"),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name="password_reset_done"),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name="password_reset_confirm"),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name="password_reset_complete"),

    path('', include('blogs_app.urls')),
]





if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





