import datetime
from django import forms
from .models import Courses,SessionYear

class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):
    Email = forms.EmailField(label="Email Address",max_length=50,widget=forms.EmailInput(attrs={'class':'form-control',"autocomplete":"off"}))
    Password = forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    ProfilePicture = forms.FileField(label="Profile Picture",max_length=50,widget=forms.FileInput(attrs={'class':'form-control'}))
    FirstName = forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    LastName = forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={'class':'form-control',"autocomplete":"off"}))
    UserName = forms.CharField(label="User Name",max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    Address = forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))

    gender_list = [("Male","Male"),("Female","Female")]
    Gender = forms.ChoiceField(label="Gender",choices=gender_list,widget=forms.Select(attrs={'class':'form-control'}))

    course_list = []
    courses = Courses.objects.all()
    for course in courses:
        course_list.append((course.id,course.course_name))

    Course = forms.ChoiceField(label="Course",choices=course_list,widget=forms.Select(attrs={'class':'form-control'}))

    sessions = SessionYear.objects.all()
    session_list = []
    for session in sessions:
        session_list.append((session.id,str(session.session_start_year)+" to "+str(session.session_end_year)))

    SessionYear = forms.ChoiceField(label="Programme Date",choices=session_list,widget=forms.Select(attrs={'class':'form-control'}))


class EditStudentForm(forms.Form):
    Email = forms.EmailField(label="Email Address",max_length=50,widget=forms.EmailInput(attrs={'class':'form-control'}))
    ProfilePicture = forms.FileField(label="Profile Picture",max_length=50,widget=forms.FileInput(attrs={'class':'form-control'}),required=False)
    FirstName = forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    LastName = forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    UserName = forms.CharField(label="User Name",max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    Address = forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))

