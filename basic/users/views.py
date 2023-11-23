from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile, Skill, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm

from .utils import searchProfiles, paginateProfiles
from django.http import JsonResponse

# Create your views here.

def loginUser(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        
        try:
            # ! import the [User] model when using this.
            user = User.objects.get(username = username)
        except :
            messages.error(request, 'username does not exist')
            # ! [authenticate()] it will take in the [username] and the [password], and it will make sure that the [password] matches the [username], and it will either use the [user] instance or it's going to return [NONE].
        # ! { user = authenticate(request, username = username, password = ) } this will query the [database] if it finds the [user] that matches the [username] and [password] then it is going to return back that user.
        user = authenticate(request, username = username, password = password)

        # ! if the [user] exists.
        if user is not None:
            # ! [ login() ] is going to create a [sessions] for the user, in the database inside the [sessions] table, then it is going to get that [sessions] and add it to our browsers [cookies]
            login(request, user)
            # will send the user to the next route.
            # * the next route will be what we have passed in the url.
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username OR Password is incorrect')
    return render(request, 'users/login_register.html')







def logoutUser(request):
# ! [logout]it is going to take in the request and the simply delete the [sessionID]
    # ! logout(request) it is going to delete that session
    logout(request)
    messages.info(request, 'User was logged out.')
    return redirect('login')



def registerUser(request):
    page = 'register'
    form  = CustomUserCreationForm()
    
    if request.method == 'POST':
        form  = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # ! convert the [username] to lowercase.
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account was created!')
            
            login(request, user)
            
            
            # return redirect('profiles')

            # * When the user create thier account they should be redirected to the edit page.
            return redirect('edit-account')


        else:
            messages.error(request, 'An error has occured during registration')
    context = {'page' : page, 'form' : form}
    return render(request, 'users/login_register.html', context)




def profiles(request):
    # ! the [searchProfiles] was decleared in the utils file check it to know more about the function.
    # ! it should return us a queryset
    profiles, search_query = searchProfiles(request)
    


# Serialize the list of Python objects to JSON.

 
    
      # ! (request, projects, 1) we are going to show 1 results each time, which is the results to be shown.
    custom_range, profiles = paginateProfiles(request, profiles, 3)
    
    # ! ['search_query' : search_query] means that we want what we have searched to be in the input form
   
    context  = {'profiles' : profiles, 'search_query' : search_query, 'custom_range' : custom_range}
    return render(request, 'users/profiles.html', context)






def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    
    
  
    
    # ! [topSkills] are skills that have description.
    # ! [description__exact=""] means that if the skills does'nt have a description exclude it.
    topSkills = profile.skill_set.exclude(description__exact="")

    # ! [otherSkills] are skills that you dont have description for.
    otherSkills = profile.skill_set.filter(description="")
    
    context   = {'profile' : profile,
                'topSkills' : topSkills,
                'otherSkills' : otherSkills}
    return render(request, 'users/user-profile.html', context)






@login_required(login_url='login/')
def userAccount(request):
    # * will get us the logged in user, if u are not logged in you will not be able to access this page.
    profile = request.user.profile
    
    skills = profile.skill_set.all()
    
    # ===> ( project_set.all ) go to the profile and give me all the projects for a particular [user] OR [profile], which means the [projects] related to the [profile] will be shown.
    projects = profile.project_set.all()

    context = {'profile' : profile, 'skills' : skills, 'projects' : projects}
    return render(request, 'users/account.html', context)









@login_required(login_url='login')
def editAccount(request):
    # * Edit the logged in user
    profile = request.user.profile
    # * we need to prefill the datas using the [instance] method
    form = ProfileForm(instance = profile)
    
    if request.method == 'POST':
        form  = ProfileForm(request.POST, request.FILES, instance = profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form' : form}
    return render(request, 'users/profile_form.html', context)






@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form  = SkillForm()
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            # * will give give us the instance of the skill [object]
            skill = form.save(commit = False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully')
            return redirect('account')
        
    context = {'form' : form}
    return render(request, 'users/skill_form.html', context)








@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id = pk)
    form  = SkillForm(instance = skill)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance = skill)
        if form.is_valid():
            skill.save()
            messages.success(request, 'Skill was updated successfully')
            return redirect('account')
    context = {'form' : form}
    return render(request, 'users/skill_form.html', context)




@login_required(login_url = 'login')
def deleteSkill(request, pk):
    profile = request.user.profile
    # ! we are getting the skill from the profile, we are querying it by the [pk]
    skill  = profile.skill_set.get(id = pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was successfully deleted.')
        
        return redirect('account')
    context = {'object': skill}
    return render(request, 'delete.html', context)


@login_required(login_url = 'login')
def inbox(request):
    profile = request.user.profile
    # * Getting the recipient messages.
    messageRequests  = profile.messages.all()
    # * Counting the unread message only.
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount':unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url = 'login')
def viewMessage(request, pk):
    # * Only the authenticated user can access their message, which means when you are logged in only can access your messages.
    profile  = request.user.profile
    # * getting the messages based on the url.
    # passing the [id] as the primary key.
    message  = profile.messages.get(id=pk)
    if message.is_read == False:
        # when the ser opens the message is been read
        message.is_read = True
        # * anytime the user opens the message it is automatically saved.
        message.save()
    context = {'message' : message}
    return render(request, 'users/message.html', context)




def createMessage(request, pk):
    recipient = Profile.objects.get(id = pk)
    form  = MessageForm()
    try:
        sender  = request.user.profile
        
    except: 
        sender = None
        
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit = False)
            message.sender = sender
            message.recipient = recipient
            
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, 'Your messages was successfully sent!')
            # * You will be redirected back to the reciever account.
            return redirect('user-profile', pk = recipient.id)
    context = {'recipient' : recipient, 'form' : form}
    return render(request, 'users/message_form.html', context)