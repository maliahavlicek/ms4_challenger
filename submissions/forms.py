from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from .models import Submission


class CreateFreeEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    image_file = forms.ImageField(label="Example Image", required=True)

    class Meta:
        model = Submission
        fields = [
            'title',
            'image_file',
        ]


class CreateBlastOff(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    image_file = forms.ImageField(label="Image File", required=True)
    audio_file = forms.FileField(label="Audio File", required=False)

    class Meta:
        model = Submission
        fields = [
            'title',
            'image_file',
            'audio_file',
        ]


class CreateInterstellar(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    image_file = forms.ImageField(label="Image File", required=True)
    audio_file = forms.FileField(label="Audio File", required=False)
    video_file = forms.FileField(label="Video File", required=False)

    class Meta:
        model = Submission
        fields = [
            'title',
            'image_file',
            'audio_file',
            'video_file',
        ]

