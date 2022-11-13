from venv import create
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects




# Create your views here.


def projects(request):
    projects, search_query =  searchProjects(request)
    # ! (request, projects, 2) we are going to show 2 results each time,
    # ! 
    custom_range, projects = paginateProjects(request, projects, 6)
        
    # ! ['search_query' : search_query] means that we want what we have searched to be in the input form, so what you searched will be in left in the search input when you search a project.
    context = {'projects': projects, 'search_query' : search_query, 'custom_range' : custom_range}
    return render(request, 'basicapp/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    
    # * ReviewForm 
    form = ReviewForm()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review  = form.save(commit = False)
        review.project = projectObj
        # * it will give us the owner
        review.owner = request.user.profile
        review.save()
        # that is the usefullness of the (@property) decorator
        projectObj.getVoteCount
        
        messages.success(request, 'Your review was submitted successfully!')
        # To clear the form after submitting the form.
        return redirect('project', pk=projectObj.id)
        
        # ! Update project vote count
    # =====> related_name = 'reviews' 
    
    # ===> this is saying give me all the child of review
    # This is a OnetoMany relationship
    # ===> ( projectObj.review ) accessing the review model [Review] is capital letter changed to small letter.
    # ===> ( review_set.all ) go to the project and give me all the reviews in the project
    # getting all the children
    
    # reviews = projectObj.review_set.all()
    
    
    # using the related name
    # reviews = projectObj.reviews.all()
    # context = {'projectObj' : projectObj, 'tags' : tags, 'reviews' : reviews}
    
    # context = {'project' : project}
    return render(request, 'basicapp/single-projects.html', {'project': projectObj, 'form': form})


# ===> views to use the model form
@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', " ").split()
        
        # print('FORM DATA', request.POST)
        # pass in the post data
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # * it will give us the instance of the current project.
            project  = form.save(commit = False)
            # * this is a OnetoMany relationship
            
            
            # ! we want the project created to be saved to the account of the person that create it or user that create the project.
            # ! project is assigned to the user that create the project.
            project.owner = profile
            project.save()
            
            for tag in newtags:
                # * create a new tag or get that particular that was already existing in the database.
                tag, created = Tag.objects.get_or_create(name=tag)
                # manytomany relationship -> adding to the tag either created or get.
                # adding the tag that was created back to the database.
                # added to the project.
                project.tags.add(tag)
                messages.info(request, tag, 'was added')
            return redirect('account')
        
    
    # pass in the form in the template
    context = {'form' :form}
    return render(request, 'basicapp/project-form.html', context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    # ! we are querying only that users profiles
    # ! only the owner can update the project
    #  ? [project_set] ? means we are getting all the childrens, so [_set] will give us all the projects for a specific profile -> [user].
    project = profile.project_set.get(id = pk)
    # project = Project.objects.get(id = pk)
    
    # the project will be prefilled
    form  = ProjectForm(instance=project)
    # we need to know the update we are updating
    
    template = 'basicapp/project-form.html'

    if request.method == 'POST':
        
        # ! Getting the tags that will be updated.
        newtags = request.POST.get('newtags').replace(',', " ").split()
        # print("DATA:", request.POST)
        # print("DATA:", newtags)
        
        # if you dont pass in the instance it will create another form but only want to update
        form = ProjectForm(request.POST,  request.FILES, instance = project)
        if form.is_valid(): 
            form.save()
            for tag in newtags:
                # * create a new tag or get that particular that was already existing in the database.
                tag, created = Tag.objects.get_or_create(name=tag)
                # manytomany relationship -> adding to the tag either created or get.
                # adding the tag that was created back to the database.
                # added to the project.
                project.tags.add(tag)
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