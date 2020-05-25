from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from .models import Entry


class CreateFreeEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    image_file = forms.ImageField(label="Example Image", required=True)

    class Meta:
        model = Entry
        fields = [
            'title',
            'image_file',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('image_file', css_class='form-group col-md-6 mb-0'),
                HTML(
                    '<div class="form-group col-md-6 mb-0">{% if entry.image_file %}<img class="mx-auto img-fluid" src="{{entry.image_file.url}}" alt="Your Entry Image for challenge." />{% endif %}</div>'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit Entry'),
            Submit('cancel', 'Cancel', css_class='btn-cancel')
        )


class CreateBlastOffEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    image_file = forms.ImageField(label="Image File", required=True)
    audio_file = forms.FileField(label="Audio File", required=False)

    class Meta:
        model = Entry
        fields = [
            'title',
            'image_file',
            'audio_file',
        ]

    def clean_image_file(self):
        """custom validation for making sure a file is uploaded"""
        image_file = self.cleaned_data.get('image_file')
        audio_file = self.cleaned_data.get('audio_file')
        if not image_file and not audio_file:
            raise forms.ValidationError('You must upload a file to submit an entry.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('image_file', css_class='form-group col-md-6 mb-0'),
                HTML(
                    '<div class="form-group col-md-6 mb-0">{% if entry.image_file %}<img class="mx-auto img-fluid" src="{{entry.image_file.url}}" alt="Your Entry Image for challenge." />{% endif %}</div>'),
                css_class='form-row'
            ),
            Row(
                Column('audio_file', css_class='form-group col-md-6 mb-0'),
                HTML(
                    '<div class="form-group col-md-6 mb-0">{% if entry.audio_file %}<audio controls><source src="{{entry.audio_file.url}}" type="audio/mp3" /><p>Your browser does not support HTML5 audio.</audio>{% endif %}</div>'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit Entry'),
            Submit('cancel', 'Cancel', css_class='btn-cancel')

        )


class CreateInterstellarEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    image_file = forms.ImageField(label="Image File", required=False)
    audio_file = forms.FileField(label="Audio File", required=False)
    video_file = forms.FileField(label="Video File", required=False)

    class Meta:
        model = Entry
        fields = [
            'title',
            'image_file',
            'audio_file',
            'video_file',
        ]

    def clean_image_file(self):
        """custom validation for making sure a file is uploaded"""
        image_file = self.cleaned_data.get('image_file')
        audio_file = self.cleaned_data.get('audio_file')
        video_file = self.cleaned_data.get('video_file')
        if not image_file and not audio_file and not video_file:
            raise forms.ValidationError('You must upload a file to submit an entry.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('image_file', css_class='form-group col-md-6 mb-0'),
                HTML(
                    '<div class="form-group col-md-6 mb-0">{% if entry.image_file %}<img class="mx-auto img-fluid" src="{{entry.image_file.url}}" alt="Your Entry Image for challenge." />{% endif %}</div>'),
                css_class='form-row'
            ),
            Row(
                Column('audio_file', css_class='form-group col-md-6 mb-0'),
                HTML(
                    '<div class="form-group col-md-6 mb-0">{% if entry.audio_file %}<audio controls><source src="{{entry.audio_file.url}}" type="audio/mp3" /><p>Your browser does not support HTML5 audio.</audio>{% endif %}</div>'),
                css_class='form-row'
            ),
            Row(
                Column('video_file', css_class='form-group col-md-6 mb-0'),
                HTML(
                    '<div class="form-group col-md-6 mb-0">{% if entry.video_file %}<video controls><source src="{{entry.video_file.url}}" type="video/mp4" /><p>Your browser does not support HTML5 video.</video>{% endif %}</div>'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit Entry'),
            Submit('cancel', 'Cancel', css_class='btn-cancel')
        )
