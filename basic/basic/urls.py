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
    path('admin/', admin.site.urls),
    path('basicapp/', include('basicapp.urls')),
    path('', include('users.urls')),
   
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)