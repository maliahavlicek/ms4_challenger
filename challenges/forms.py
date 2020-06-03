from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from storages.backends.s3boto3 import S3Boto3StorageFile

from .models import Challenge
from accounts.forms import DateInput
from datetime import date
import os
from django.template.defaultfilters import filesizeformat



class CreateChallengeForm(forms.Form):
    """
    Form for Create challenge
    """
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)
    example_image = forms.ImageField(label="Example Image")
    example_video = forms.FileField(label="Example Video", required=False)
    members = forms.CharField(widget=forms.HiddenInput(), required=False)
    submission_types = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Submission Type(s)")

    class Meta:
        model = Challenge
        fields = [
            'name',
            'description',
            'start_date,'
            'end_date',
            'example_image',
            'example_video',
            'members',
            'submission_types'
        ]

    def clean(self):
        """custom validation for end_date"""
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date and end_date:
            if end_date < start_date:
                self.add_error('end_date', 'End Date must come after Start Date.')

            if end_date < date.today():
                self.add_error('end_date', 'End Date cannot be in the past.')

    def clean_example_video(self):
        video_file = self.cleaned_data.get('example_video')
        if video_file:
            valid_mime_types = ['video/mp4', 'video/quicktime']
            if isinstance(video_file, S3Boto3StorageFile):
                # aws storage MIME type check
                if video_file.obj.content_type not in valid_mime_types:
                    self.add_error('example_video', 'Unsupported file type, expecting video/mp4 or video/quicktime.')
            else:
                # local storage MIME type check
                if video_file.content_type not in valid_mime_types:
                    self.add_error('example_video', 'Unsupported file type, expecting video/mp4 or video/quicktime.')
            valid_file_extensions = ['.mp4', '.mov']
            ext = os.path.splitext(video_file.name)[1]
            if ext.lower() not in valid_file_extensions:
                self.add_error('example_video', 'Unacceptable file extension, expecting .mp4 or .mov')
            # limit videos to 50 MB
            size_limit = 52428800
            if video_file.size > size_limit:
                self.add_error('example_video', 'Please keep file size under %s. Current size %s' % (
                    filesizeformat(size_limit), filesizeformat(video_file.size)))

    def clean_example_image(self):
        image_file = self.cleaned_data.get('example_image')
        if image_file:
            # limit images to 10 MB
            size_limit = 10485760
            if image_file.size > size_limit:
                self.add_error('example_image', 'Please keep file size under %s. Current size %s' % (
                    filesizeformat(size_limit), filesizeformat(image_file.size)))

    def __init__(self, submission_choices, *args, **kwargs):
        self.submission_choices = submission_choices
        super(CreateChallengeForm, self).__init__(*args, **kwargs)
        self.fields['submission_types'].choices = self.submission_choices
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('example_image', css_class='form-group col-md-4 mb-0'),
                Column('example_video', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('start_date', css_class='form-group col-md-6 mb-0'),
                Column('end_date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                HTML(
                    '<div class="form-group col-md-6 mb-0">'
                    '<div id="div_id_submission_types" class="form-group">'
                    '<label for="div_id_submission_types requiredField" class="">Submission Types<span class="asteriskField">*</span></label>'
                    '<div class="{% if "submission_types" in challenge_form.errors %}is-invalid{% endif %}">'
                    '{% for value, text in challenge_form.submission_types.field.choices %}'
                    '<div class="field multi_select_form_field checkbox_select_multiple">'
                    '<label class="" for="id_submission_types_{{ forloop.counter0 }}">'
                    '<input type="checkbox" class="" name="submission_types" id="id_submission_types_{{ forloop.counter0 }}" value="{{value}}"'
                    '{% if challenge_form.submission_types.field.choices|length == 1 %} checked="checked"{% elif value in challenge_form.submission_types %} checked="checked"{% endif %}>'
                    '{{ text }}</label>'
                    '</div>'
                    '{% endfor %}'
                    '</div>'
                    '{% if "submission_types" in challenge_form.errors %}<span class="invalid-feedback" id="error_submission_types_list">You must select a submission type.</span>{% endif %}'
                    '</div>'
                    '</div>'
                ),
                css_class='form-row'
            ),
            Row(
                HTML('<div class="form-group col-md-12 mb-0"><label>Members</label><div id="member_list"></div></div>'),
                css_class='form-row'),
            Row(
                HTML(
                    '<div class="form-group col-md-12 mb-0"><div class="form-group"><div class id="member_list_errors"><span id="error_member_list"></span></div></div></div>'),
                HTML('<div class="form-group member-entry col-md-3 mb-0 d-none d-md-block"><div class="form-group"><div class><input class="form-control" id="first_name" type="text" aria-label="first_name" max_length="50" placeholder="First Name"/></div></div></div>'),
                HTML('<div class="form-group member-entry col-md-3 mb-0 d-none d-md-block"><div class="form-group"><div class><input class="form-control" id="last_name" type="text" aria-label="last name" max_length="50" placeholder="Last Name"/></div></div></div>'),
                HTML('<div class="form-group member-entry col-md-4 mb-0"><div class="form-group"><div class><input class="form-control member email" id="email" type="email" aria-label="email" placeholder="Email"/>'
                     '<span id="error_email"></span></div></div></div>'),
                HTML('<div class="form-group member-entry col-md-2 mb-0"><div class="form-group"><div class><a onclick="add_member();" id="add_member" class="form-control btn btn-primary"><i class="fas fa-user-plus"></i> Member</a></div></div></div>'),
                css_class='form-row'
            ),
            Row(Column('members'), css_class='form-row'),
            Row(HTML(
                '<input type="hidden" id="max_members" value="{{owned_product.max_members_per_challenge}}" />'
            ), css_class='form-row'),
            Submit('submit', 'Create Challenge'),
            Submit('cancel', 'Cancel', css_class='btn-cancel')
        )


class UpdateChallengeForm(forms.Form):
    """
    Update is basically the Create challenge form with different submit button name and no ability to change submission types
    """
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)
    example_image = forms.ImageField(label="Example Image")
    example_video = forms.FileField(label="Example Video", required=False)
    members = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Challenge
        fields = [
            'name',
            'description',
            'start_date,'
            'end_date',
            'example_image',
            'example_video',
            'members',
        ]

    def clean_end_date(self):
        """custom validation for end_date"""
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if end_date < start_date:
            raise forms.ValidationError('End Date must come after Start Date.')

        if end_date < date.today():
            raise forms.ValidationError('End Date cannot be in the past.')

    def clean(self):
        cleaned_data = super().clean()
        example_video = cleaned_data.get('example_video')
        if example_video:
            valid_mime_types = ['video/mp4', 'video/quicktime']
            if isinstance(example_video, S3Boto3StorageFile):
                # aws storage MIME type check
                if example_video.obj.content_type not in valid_mime_types:
                    self.add_error('example_video', 'Unsupported file type, expecting video/mp4 or video/quicktime.')
            else:
                # local storage MIME type check
                if example_video.content_type not in valid_mime_types:
                    self.add_error('example_video', 'Unsupported file type, expecting video/mp4 or video/quicktime.')

            valid_file_extensions = ['.mp4', '.mov']
            ext = os.path.splitext(example_video.name)[1]
            if ext.lower() not in valid_file_extensions:
                self.add_error('example_video', 'Unacceptable file extension, expecting .mp4 or .mov')
            # limit videos to 50 MB
            size_limit = 52428800
            if example_video.size > size_limit:
                self.add_error('example_video', 'Please keep file size under %s. Current size %s' % (
                    filesizeformat(size_limit), filesizeformat(example_video.size)))

            image_file = self.cleaned_data.get('example_image')
            if image_file:
                # limit images to 10 MB
                size_limit = 10485760
                if image_file.size > size_limit:
                    self.add_error('example_image', 'Please keep file size under %s. Current size %s' % (
                        filesizeformat(size_limit), filesizeformat(image_file.size)))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('example_image', css_class='form-group col-md-6 mb-0'),
                HTML(
                    '<div class="form-group col-md-6 mb-0"><label for="example_image">Example Image</label><img id="example_image" class="mx-auto img-fluid" src="{{challenge.example_image.url}}" alt="Example Image for challenge." /></div>'),
                css_class='form-row'
            ),
            Row(
                Column('example_video', css_class='form-group col-md-6 mb-0'),
                HTML(
                    '{%if challenge.example_video %}<div class="form-group col-md-6 mb-0"><label for="example_video">Example Video"</label><video id="example_video" width="100%" height="auto" controls><source src="{{challenge.example_video.url}}"'
                    'Your browser does not support the HTML5 video tag</video></div>{% endif %}'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('start_date', css_class='form-group col-md-6 mb-0'),
                Column('end_date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                HTML(
                    '<div class="form-group col-md-6 mb-0">'
                    '<div class="form-group">'
                    '<label for="div_id_submission_types" class="">Submission Types</label>'
                    '<div id="div_id_submission_types" class=""><ul>{% for type in challenge.submission_types %}<li>{{type}}</li>{% endfor %}</ul><p>Submission Types are not editable.</p>'                    
                    '</div>'
                    '</div>'
                    '</div>'
                ),
                css_class='form-row'
            ),
            Row(
                HTML('<div class="form-group col-md-12 mb-0"><label>Members</label><div id="member_list"></div></div>'),
                css_class='form-row'),
            Row(
                HTML(
                    '<div class="form-group col-md-12 mb-0"><div class="form-group"><div class id="member_list_errors"><span id="error_member_list"></span></div></div></div>'),
                HTML(
                    '<div class="form-group member-entry col-md-3 mb-0"><div class="form-group"><div class><input class="form-control" id="first_name" type="text" aria-label="first_name" max_length="50" placeholder="First Name"/></div></div></div>'),
                HTML(
                    '<div class="form-group  member-entry col-md-3 mb-0"><div class="form-group"><div class><input class="form-control" id="last_name" type="text" aria-label="last name" max_length="50" placeholder="Last Name"/></div></div></div>'),
                HTML(
                    '<div class="form-group member-entry col-md-4 mb-0"><div class="form-group"><div class><input class="form-control" id="email" type="email" aria-label="email" placeholder="Email"/>'
                    '<span id="error_email"></span></div></div></div>'),
                HTML(
                    '<div class="form-group member-entry col-md-2 mb-0"><div class="form-group"><div class><a onclick="add_member();" id="add_member" class="form-control btn btn-primary"><i class="fas fa-user-plus"></i> Member</a></div></div></div>'),
                css_class='form-row'
            ),
            Row(HTML(
                '<input type="hidden" id="max_members" value="{{owned_product.max_members_per_challenge}}" />'
            ), css_class='form-row'),
            Row(Column('members'), css_class='form-row'),
            Submit('submit', 'Save Changes'),
            Submit('cancel', 'Cancel', css_class='btn btn-cancel')
        )
