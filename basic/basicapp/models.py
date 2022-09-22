from django.db import models
import uuid
from django.core.validators import FileExtensionValidator
from users.models import Profile


# Create your models here.
# Create a user in your database.
# We are using models for our table.


# ===> ( null = True) means that the item can be added to the database and it can be empty.
# ===> ( blank = True) means that you want django know that you can submit a form and and it can be blank.
# ===> ( unique=True ) no other project can have the same id.
# ===> ( primary_key=True ) telling django this is now our primary key of id.



class Project(models.Model):
    # ! we want to connect a [project] to a specific user, that should be a [manytoone] relationship.
    owner               = models.ForeignKey(Profile, null=True,blank=True, on_delete=models.SET_NULL)
    title               = models.CharField(max_length=200)
    description         = models.TextField(null=True, blank=True)
    featured_image      = models.ImageField(validators = [FileExtensionValidator(['png', 'jpg'])], null=True, blank=True, default='default.jpg')
    demo_link           = models.CharField(max_length=1000, null=True, blank=True)
    source_link         = models.CharField(max_length=1000, null=True, blank=True)
    vote_total          = models.IntegerField(default=0)
    # Ratio between the ratio and the type of vote
    vote_ratio          = models.IntegerField(default=0)
    tags                = models.ManyToManyField('Tag', blank=True)
    # Timestamp of when the model was instantiated
    created             = models.DateTimeField(auto_now_add=True)
    # uuid is very secure to use in django, and they are always unique.
    # uuid4 will generate a more unique id because they are all versions, we are using verson 4.
    # Strength of the string is larger than the other one.
    id                  = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    
    
    def __str__(self):
        return self.title
    
    # ! Order by day OR date, it will display the projects by the datetime or date that are created
    class Meta:
        # [-created] descending and ascending [created] order.
        # * Order by data created.
        ordering  = ['-vote_ratio', '-vote_ratio', 'title']
        
        #will be use on the templates
    @property 
    def reviewers(self):
        # getting a single attributes of the reviews 
        # ** [flat()] will convert it into a full list
        # wiil give us the entire ids of people that have reviwed
        
        queryset = self.review_set.all().values_list('owner__id', flat = True)
        return queryset
        
        
        
        # * Calculate the amount of vote
    @property
    def getVoteCount(self):
    # getting all the reviews
        reviews = self.review_set.all()
        # * getting the reviews that has the [up -> vote]
        # * counting the reviews that is upvoted.
        upVotes = reviews.filter(value = 'up').count()
        # *Counting all the reviews
        totalVotes = reviews.count()
        ratio  = (upVotes / totalVotes) * 100
        # * result accumulated will be display to the users, the calculations that was done.
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()

 
    
class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'up'),
        ('down', 'down'),
    )
    
    
    # One-to-One
    owner           = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    # use the related_name we be use to access it .
    project         = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank='True')  # SET_NULL -> will set it to null when u delete the parent model
    
    # project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews')  # SET_NULL -> will set it to null when u delete the parent model
    
    
    
    body             = models.TextField(null=True, blank=True)
    # we want this to be a dropdown to allow the user select what they want.
    # when the user is using this they cant have there own value they can only select
    value            = models.CharField(max_length=50, choices=VOTE_TYPE)
    # Anytime you update it
    updated          = models.DateTimeField(auto_now = True)
    created          = models.DateTimeField(auto_now_add=True)
    id               = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    class Meta:
        # * A user can only review once on a single project
        # it is now unique to each other
        # * [ unique_together ] means only a owner can only review a particular project once.
        unique_together     = [['owner', 'project']]

    def __str__(self):
        return self.value
    
    
class Tag(models.Model):
    # we dont want it to be blank
    name        = models.CharField(max_length=200)
    created     = models.DateTimeField(auto_now_add=True)
    id          = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    


    def __str__(self):
        return self.name