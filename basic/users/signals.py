# ! it will trigger when a model is save or deleted of about to be saved.
from django.db.models.signals import post_save, post_delete

from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

from django.core.mail import send_mail
# * want the email to be dynamic, anyone can send the email.
from django.conf import settings



# * Don't forget to let django know that you are using the signals.py, so you should set it in the [apps.py]



#*****************************************************************************************************#
 # ! [sender] is the model that actually send the message.
 # ! [instance] it the instance of the model that actually trigger it.
 # ! [created] will let you know whether it true of false, if a user was added of a model was added to the database or saved again.
 # ! [**kwargs] this is our function.      
# ******************************************************************************************#
def createProfile(sender, instance, created, **kwargs):
    # ! checking if it is the first instance of the user
    if created:
        user = instance
        # ! creating a profile
        profile = Profile.objects.create(
            # ! connecting the profile to the new user that just trigger this.
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name
        )
        subject = 'Welcome to DeVConnect'
        message = 'Very glad you are here'
        send_mail(
            subject,
            message,
            # the person that is send the email
            # the message wll be sent from the company that owns the website.
            settings.EMAIL_HOST_USER,
            # the recipient or the reciver of the email, get the from the person profile which means the the person creating the account.
            [profile.email],
            fail_silently = False,
        )

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    # *if we dont put the conditional statement there the user updated will be created again, it will trigger the [createProfile] method.
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()
    
    
# ! Anytime we delete a profile we also wants to delete a user.
def deleteUser(sender, instance, **kwargs):
    try:
        user  = instance.user
        user.delete()
    except:
        pass
    

# ! Anytime a user [model] get created, a profile will get created
post_save.connect(createProfile, sender = User)
# Anytime the user is updated
post_save.connect(updateUser, sender = Profile)

post_delete.connect(deleteUser, sender = Profile)





# *   if you dont use the one's below you can use a [receiver] instead.

# ! [sender = Profile] is the model that is going to trigger this, which means anytime the save method which is [post_save] is called on a [Profile] model, so after the save method is complete that model is saved, we are going to trigger the [profileUpdated] method
# post_save.connect(profileUpdated, sender = Profile)




# ! is going to trigger anytime a [profile] is deleted
# ! when a profile is deleted we 
# post_delete.connect(deleteUser, sender = Profile)