from django.urls import path
from . import views 

'''
/**
* ! This wont work now you have to go your root urls to include it.
* 
*
*
*
*
*/
'''
urlpatterns = [
    path('', views.projects, name="projects"),
    
    # when you change the path name you will have to change it in the link tag also so the best thing to do is to use the name attribute in the link 
    path('project/<str:pk>/', views.project, name="project"),
    path('create-project', views.createProject, name = "create-project"),
    # we want to update a single project
    path('update-project/<str:pk>/', views.updateProject, name = "update-project"),
    path('delete-project/<str:pk>/', views.deleteProject, name = "delete-project")    
]