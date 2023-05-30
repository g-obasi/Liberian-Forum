from django.forms import ModelForm, Form
from django import forms

from .models import Topic, Post, Board, Attachment


class TopicForm(ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'rows': 5, 'id': 'postformtitle', 'placeholder': '100 words or less'}))
    message = forms.CharField(max_length=4096, widget=forms.Textarea(
    attrs={'rows': 12, 'id': 'body1', 'placeholder': '4000 words or less'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True}))
    # file = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True}))

    class Meta:
        model = Topic
        fields = ['title', ]




class BoardChoiceForm(Form):
    board_select = Board.objects.values_list('id', 'name')
    # board_choices = ((x.id, x.name) for x in board_select)
    select_board = forms.ModelChoiceField(
        queryset=board_select,  label=None)
#    select_board = forms.ChoiceField(choices=board_choices,  label=None)


# Reply Topic
class PostForm(ModelForm):
    message = forms.CharField(max_length=4096, widget=forms.Textarea(
    attrs={'rows': 12, 'id': 'body1', 'placeholder': '4000 words or less'}))
    file = forms.FileField(required=False, widget=forms.FileInput(attrs={'multiple': True}))

    class Meta:
        model = Post
        fields = ['message', 'file']


class FileForm(ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True}))

    class Meta:
        model = Attachment
        fields = ['file', ]


class PostUpdateForm(ModelForm):
    message = forms.CharField(max_length=4096, widget=forms.Textarea(
        attrs={'rows': 12, 'id': 'body1', 'placeholder': '4000 words or less'}))
    file = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}))

    class Meta:
        model = Post
        fields = ['message', 'file' ]


class SearchForm(Form):
    
    # board_choices =((x.id, x.name) for x in board_select)  
    # board_objects= Board.objects.values_list('id', 'name', flat=True) # When calling call with *board_objects

    board_select = Board.objects.values_list('id', 'name')
    search_input = forms.CharField(max_length=90)
    select_board = forms.ModelChoiceField(
    queryset=board_select,  label=None)    
    search_topics_only = forms.BooleanField()
    search_images_only = forms.BooleanField()


# Quote post
class QuoteForm(ModelForm):
    message = forms.CharField(max_length=2048, widget=forms.Textarea(
        attrs={'rows': 12, 'id': 'body1', 'placeholder': '2000 words or less'}))
    file = forms.FileField(required=False, widget=forms.FileInput(attrs={'multiple': True}))

    class Meta:
        model = Post
        fields = ['message', ]
