# * Wiil turn all our pytho data to [json].
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

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