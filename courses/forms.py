from django import forms
from courses.models import Course, Lesson, Feedback


class AddCourseForm(forms.ModelForm):
    title = forms.CharField(max_length=20, widget=forms.TextInput(attrs=({
        'placeholder': 'Title',
        'class': 'form-control',
    })))
    description = forms.CharField(max_length=50, widget=forms.Textarea(attrs=({
        'class': 'form-control',
    })))
    schedule = forms.CharField(max_length=20, widget=forms.TextInput(attrs=({
        'class': 'form-control',
    })))

    class Meta:
        model = Course
        fields = ['title', 'description', 'creator', 'schedule']


# class AddSectionForm(forms.ModelForm):
#     class Meta:
#         model = Section
#         fields = "__all__"


class AddLessonForm(forms.ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs=({
        'placeholder': 'Title',
        'class': 'form-control',
    })))

    description = forms.CharField(max_length=50, widget=forms.Textarea(attrs=({
        'class': 'form-control',
    })))
    description1 = forms.CharField(widget=forms.Textarea(attrs=({
        'class': 'form-control',
    })))

    class Meta:
        model = Lesson
        fields = "__all__"


class EnrollForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['key']

class AddFeedbackForm(forms.ModelForm):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs=({
        'placeholder': 'Title',
        'class': 'form-control',
    })))
    description = forms.CharField(max_length=50, widget=forms.Textarea(attrs=({
        'class': 'form-control',
    })))

    class Meta:
        model = Feedback
        fields = "__all__"