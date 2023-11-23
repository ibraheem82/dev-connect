# All the model form will be stored in this section
# from dataclasses import field
# from dataclasses import field
from django.forms import ModelForm

# ! the [form] imported will allow us add widget and style our [modelForm] in a customizable way.
from django import forms
from .models import Project, Review

# To use it model form import it in your view

# ===> ( ModelForm ) will make it a model form
class ProjectForm(ModelForm):
    class Meta:
         model = Project
        #  fields = '__all__'
         fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        #  we are excluding this fields
         exclude = ['vote_total', 'vote_ratio']
         
         
         widgets = {
            #  !  it will turn the [tags] into a checkbox.
             'tags': forms.CheckboxSelectMultiple(),
         }
         
        # ! Adding classes to the form.
    def __init__(self, *args, **kwargs):
        # ! [ProjectForm] means telling it the class we are modifying or overriding it.
        super(ProjectForm, self).__init__(*args, **kwargs)
        
        # ! we are selecting the [names] of each fields and widget with the attributes of ['class':'input']
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        
            
        # ! Selecting the actual field that we want to modify
        # ! we are updating the [title] class attributes to [input]
        # self.fields['title'].widget.attrs.update(
        #     {'class':'input'}
        #      )
        
        
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote'
            
            }    
        # ! Adding classes to the form.
    def __init__(self, *args, **kwargs):
        # ! [ReviewForm] means telling it the class we are modifying or overriding it.
        super(ReviewForm, self).__init__(*args, **kwargs)
        
        # ! we are selecting the [names] of each fields and widget with the attributes of ['class':'input']
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})