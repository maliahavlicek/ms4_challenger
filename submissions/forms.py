from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from .models import Entry
import os
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat

FILE_SIZE_TO_BYTES = {
    2.5: 2621440,
    5: 5242880,
    10: 10485760,
    20: 20971520,
    50: 5242880,
    100: 104857600,
    250: 214958080,
    500: 429916160
}


class CreateEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    image_file = forms.ImageField(label="Image File", required=False)
    audio_file = forms.FileField(label="Audio File", required=False)
    video_file = forms.FileField(label="Video File", required=False)
    submission_size_limit = forms.IntegerField(widget=forms.HiddenInput())
    submission_time_limit = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Entry
        fields = [
            'title',
            'image_file',
            'audio_file',
            'video_file',
        ]

    def clean(self):
        cleaned_data = super().clean()
        size_limit = FILE_SIZE_TO_BYTES[cleaned_data.get('submission_size_limit')]
        audio_file = cleaned_data.get('audio_file')
        if audio_file:
            valid_mime_types = ['audio/mp3', 'audio/mpeg']
            if audio_file.content_type not in valid_mime_types:
                self.add_error('audio_file', 'Unsupported file type, expecting audio/mp3 or audio/mpeg.')
            valid_file_extensions = ['.mp3']
            ext = os.path.splitext(audio_file.name)[1]
            if ext.lower() not in valid_file_extensions:
                self.add_error('audio_file', 'Unacceptable file extension, expecting .mp3')

            if audio_file.size > size_limit:
                self.add_error('audio_file', 'Please keep file size under %s. Current size %s' % (
                    filesizeformat(size_limit), filesizeformat(audio_file.size)))

        video_file = cleaned_data.get('video_file')
        if video_file:
            valid_mime_types = ['video/mp4']
            if video_file.content_type not in valid_mime_types:
                self.add_error('video_file', 'Unsupported file type, expecting video/mp4.')
            valid_file_extensions = ['.mp4']
            ext = os.path.splitext(video_file.name)[1]
            if ext.lower() not in valid_file_extensions:
                self.add_error('video_file', 'Unacceptable file extension, expecting .mp4')
            if video_file.size > size_limit:
                self.add_error('video_file', 'Please keep file size under %s. Current size %s' % (
                    filesizeformat(size_limit), filesizeformat(video_file.size)))

        image_file = cleaned_data.get('image_file')
        if image_file:
            if image_file.size > size_limit:
                self.add_error('image_file', 'Please keep file size under %s. Current size %s' % (
                    filesizeformat(size_limit), filesizeformat(image_file.size)))

        # must have at least one file in POST to be valid
        if not video_file and not audio_file and not image_file:
            raise ValidationError("You must upload a file for your entry.")

    def __init__(self, submission_types, *args, **kwargs):
        self.submission_types = submission_types
        super(CreateEntryForm, self).__init__(*args, **kwargs)
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
                css_class='form-row image-file'
            ),
            Row(
                Column('audio_file', css_class='form-group col-md-6 mb-0'),
                HTML(
                    '<div class="form-group col-md-6 mb-0">{% if entry.audio_file %}<audio controls><source src="{{entry.audio_file.url}}" type="audio/mp3" /><p>Your browser does not support HTML5 audio.</audio>{% endif %}</div>'),
                css_class='form-row audio-file'
            ),
            Row(
                Column('video_file', css_class='form-group col-md-6 mb-0'),
                HTML(
                    '<div class="form-group col-md-6 mb-0">{% if entry.video_file %}<video controls><source src="{{entry.video_file.url}}" type="video/mp4" /><p>Your browser does not support HTML5 video.</video>{% endif %}</div>'),
                css_class='form-row video-file'
            ),
            Row(
                Column('submission_size_limit', css_class='form-group col-md-6 mb-0'),
                Column('submission_time_limit', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Submit Entry'),
            Submit('cancel', 'Cancel', css_class='btn-cancel')
        )
