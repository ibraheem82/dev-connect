"""basic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


from django.conf import settings
# [static] is going to help us create a url for our static files
from django.conf.urls.static import static
# from django.http import HttpResponse

# * To be able to implement password reset (authentication views).
from django.contrib.auth import views as auth_views

# # ###################
# '''
# /**
# * TODO: (request) handles all our http response
# * @param path('projects', project) -> when you create a view you must create the the url at the same time
# * You can add a dynamic values <int> <str> <slug> and the values can be be anything it can be cookies, or pk
# *
# *
# *
# */


# '''
# ########################
# def projects(request):
#     return HttpResponse('<h1>This the projects page</h1>')

# def project(request, pk):
#     # You can query data and render a dynamic values to the url
#     return HttpResponse('<h2>This the project page</h2>' + str(pk))
    

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('secure-login/', admin.site.urls),
    path('basicapp/', include('basicapp.urls')),
    path('', include('users.urls')),
    # ! <api->[urls]> urls for our apis
    path('api/', include('api.urls')),
    
    
    
    # will link up to the password rest form
    # * be very careful about the naming conventions.
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "reset_password.html"), name = 'reset_password'),
    
    
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "reset_password_sent.html"), name = 'password_reset_done'),


    # * [<uidb64>] : will encode the user id in the base<64> encryption
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "reset.html"), name = 'password_reset_confirm'),


    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name = "reset_password_complete.html"), name = 'password_reset_complete'),
   
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)