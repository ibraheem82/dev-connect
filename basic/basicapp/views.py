from unicodedata import name
from unittest import result
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Project, Tag
from .forms import ProjectForm
from .utils import searchProjects




# Create your views here.


def projects(request):
    projects, search_query =  searchProjects(request)
    # ! Getting the first page
    # page = 1
    # ! Getting the seccond page
    # page = 2
    
    # todo-> the page must be an integer, it will be pass in to the paginator button so it will display the number of the page on the browser search url and show the page we are on.
    page = request.GET.get('page')
    
    
    # ! Numbers of page to be paginated
    # ! Give us 3 results per page
    results = 3
    # ! it will give us the query_set and give us the [results] here
    # ! it will give us three results per page.
    paginator = Paginator(projects, results)
    
    try:
        # !Resetting the project variable and index it by a specific page and only get 3 results
        # ! we are going to get 3 projects and we are going to get the first page of those 3 projects
        # ! [ .page ] means what page do we want to get from the query_set
        projects = paginator.page(page)
        # ! [ PageNotAnInteger ] it means that if a page is not passed in, it should be set to 1, we are saying that if the user click on the [projects] link on the navigation bar it should set it to the first page
    except PageNotAnInteger:
        page = 1
        # ! if a user click on the page or just visting the page for the first time it will display the first page which we have set.
        projects = paginator.page(page)
        # ! if the user keep searching the page and there is no more page
        # ! we are saying that if there is no page, so if the user go out of page, it will give the user the last page
    except EmptyPage:
        # ! [  num_pages ] this will tell us how many pages we have
        page = paginator.num_pages
        # ! setting projects to the page value, it is going to give us whatever the last page is.
        projects = paginator.page(page)
        
    
    context = {'projects': projects, 'search_query' : search_query}
    return render(request, 'basicapp/projects.html', context)

def project(request, pk):

    
    # ===> to get a single object from the database
    project = Project.objects.get(id=pk)
    # for i in projectsList:
    #      if i['id'] == str(pk):
    #          projectObj = i
    
    # ===> you can specify the parent name
    # tags = projectObj.tags.all()
    # ===> this is saying give me all the child of review
    # This is a OnetoMany relationship
    # ===> ( projectObj.review ) accessing the review model Review is cpaital letter
    # ===> ( review_set.all ) go to the project and give me all the reviews in the project
    # getting all the children
    
    
    
    # =====> related_name = 'reviews'
    
    
    
    
    
    
    
    # reviews = projectObj.review_set.all()
    
    
    
    # using the related name
    # reviews = projectObj.reviews.all()
    # context = {'projectObj' : projectObj, 'tags' : tags, 'reviews' : reviews}
    
    
    # we want to access it in the templates without using the tags and the review in the templates
    
    context = {'project' : project}
    return render(request, 'basicapp/single-projects.html', context)


# ===> views to use the model form
@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    
    if request.method == 'POST':
        # print('FORM DATA', request.POST)
        # pass in the post data
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # * it will give us the instance of the current project.
            project  = form.save(commit = False)
            # * this is a OnetoMany relationship
            
            
            # ! we want the project created to be saved to the account or user that create the project
            # ! project is assigned to the user that create the project.
            project.owner = profile
            project.save()
            return redirect('account')
        
    
    # pass in the form in the template
    context = {'form' :form}
    return render(request, 'basicapp/project-form.html', context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    # ! we are querying only that users profiles
    # ! only the owner can update the project
    #  ? [project_set] ? means we are getting all the childrens, so [_set] will give us all the projects  
    project = profile.project_set.get(id = pk)
    # project = Project.objects.get(id = pk)
    
    # the project will be prefilled
    form  = ProjectForm(instance=project)
    # we need to know the update we are updating
    
    template = 'basicapp/project-form.html'
    
    if request.method == 'POST':
        # if you dont pass in the instance it will create another form but only want to update
        form = ProjectForm(request.POST,  request.FILES, instance = project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form' : form}
    
    return render(request, template, context)


@login_required(login_url="login")
def deleteProject(request, pk):
    
    profile = request.user.profile
    
    # ! only logged in user can delete the project
    # getting the object by the primary key
    project = profile.project_set.get(id = pk)
    # project = Project.objects.get(id = pk)
    if request.method == 'POST':
        # it will remove the project from the database
        project.delete()
        return redirect('projects')
    return render(request, 'delete.html', {'object': project})