from rest_framework import serializers
from basicapp.models import Project, Tag, Review
from users.models import Profile


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

# * Serializing the model
# * it will also convert it into a json objects
class ProjectSerializer(serializers.ModelSerializer):
    # This is connected to a profile.
    # it will use the ProfileSerializer and return back a object.
    owner = ProfileSerializer(many = False)
    # we want multiple tags.
    tags = TagSerializer(many = True)
    # will add attribute just to the serializer
    reviews = serializers.SerializerMethodField()
    
    # total_votes = serializers.SerializerMethodField()
    class Meta:
        model = Project
        # These fields has been serialized.
        fields = '__all__'

        # creating a method for the review()
        # ** our method
        # here should start with  [    get_  ]
        # it has to start with that if you want to use the SerializerMethodField

        # the [sel] is going to refer to the ProjectSerializer class()
        # [obj] is the object that we are serializing which is the [Project]
    def get_reviews(self, obj):
        # it get all of the project reviews.
        reviews = obj.review_set.all()
        
        # @@ Serializing it
        serializer  = ReviewSerializer(reviews, many = True)
        # we are returning a queryset of reviews but at the same time the serialized one
        return serializer.data

    
    # def get_total_votes(self, obj):
    #     # it get all of the project reviews.
    #     total_votes = obj.vote_total()

    #     # @@ Serializing it
    #     serializer  = ReviewSerializer(total_votes, many = False)
    #     # we are returning a queryset of reviews but at the same time the serialized one
    #     return serializer.data