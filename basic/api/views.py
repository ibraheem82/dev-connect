# * Wiil turn all our pytho data to [json].
from django.http import JsonResponse
# [permission_classes] for api authentication
from rest_framework.decorators import api_view, permission_classes
# * Using class based view for the api authentication [permission_classes] class.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ProjectSerializer
from basicapp.models import Project, Review

# * by default the jsonResponse can only return a dictionary.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        # * will return back a list of project objects
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        # * Anytime a user wants to vote on a specific project, they will be send to this route or anytime they click on the route they will be send here
        {'POST': '/api/projects/id/vote'},

        # ** This will generate a token for the use 
        # * we are going to be able to generate a token for a user.
        # * this is going to allow us login a user.
        
        # * Class Based views is going t help us achieve this 
        {'POST': '/api/users/token'},
        # ** this will be for a refresh token
        # json webtoken do have an expiration date, so when a user's token expires which is going to be around five minutes, it makes should the user can still stay log     in
        {'POST': '/api/users/token/refresh'}

        ,
        {'POST': '/api/projects/id/vote'},
    ]
    # [safe = ] tells us that we can return something that is more than a python dictionary
    # return JsonResponse(routes, safe=False)
    return Response(routes)












# **This route will query the database and get our routes for us.
@api_view(['GET'])
# ! Only authenticated user can view this route.
# ! this route will be restricted to the unauthenticated user.
# @permission_classes([IsAuthenticated])
def getProjects(request):
    # print('USER👤', request.user)
    # getting all the objects.
    projects = Project.objects.all()
    # @ We need to pass in serialized data, we need to pass in json data.
    # ! this [ProjectSerializer] is taken the (projects) and turning it into a json data.
    serializer = ProjectSerializer(projects, many = True)
    # will give us the actual serialized project
    return Response(serializer.data)




@api_view(['GET'])
def getProject(request, pk):
    # getting all the objects.
    project = Project.objects.get(id=pk)
    # @ We need to pass in serialized data, we need to pass in json data.
    # ! this [ProjectSerializer] is taken the (projects) and turning it into a json data.
    serializer = ProjectSerializer(project, many = False)
    # will give us the actual serialized project
    return Response(serializer.data)




@api_view(['POST'])
# * The user must be logged in
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project  = Project.objects.get(id = pk)
    # * The user is comming from the token.
    user = request.user.profile
    data = request.data
    # print(data)
    # print(f'DATA {data}')
    
    
    # when you just created a user, a user with the attribute below will be created
    # * [get_or_create()] will check if the objects below exist in the database. for example "if the user already left a review on the particular project we are getting then it is going to get that user it is not not going to create a new one it is just going to get the user and return back an object, if that user does not exist it is going to create the user which is the Review for us."
    # review there will be true or false.
    review, created = Review.objects.get_or_create(
        owner = user,
        project = project,
    )
    # getting the object from the value and setting it.
    review.value = data['value']
    review.save()
    project.getVoteCount
    
    serializer = ProjectSerializer(project, many = False)


    
    return Response(serializer.data)