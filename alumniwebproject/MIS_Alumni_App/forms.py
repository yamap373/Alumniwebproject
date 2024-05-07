from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator
from django.forms import ModelChoiceField
from .models import *
import datetime
 

class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=120)
    last_name = forms.CharField(max_length=120)
    alumni_email = forms.EmailField(validators=[RegexValidator(r'^\d{8}26+@mis\.chula\.ac\.th$', 'Please use a valid email (format: username@mis.chula.ac.th)')])
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    
    class Meta:
        model = UserProfile
        fields = ('alumni_email', 'first_name', 'last_name')
        labels = {
            'alumni_email': 'Alumni Email(@mis.chula.ac.th)',
           
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    

class AlumniForm(forms.ModelForm):
    current_year = datetime.date.today().year
    profile_picture = forms.FileField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],required=False)
    mentor_status = forms.BooleanField(required=False, initial=False)  # Adjusted to BooleanField
    started_year = forms.IntegerField(
        min_value=datetime.date.today().year - 85,  # Minimum value 85 years ago
        max_value=datetime.date.today().year - 3,      
        label='Started Year',  # 
        required=False,
        initial=datetime.date.today().year - 3
      )  # Add started_year field
    graduated_year = forms.IntegerField(
        min_value=datetime.date.today().year-84,  # Minimum value 8 years ago
        max_value=datetime.date.today().year,       
        label='Graduated Year',  
        required=False,
        initial=datetime.date.today().year-1
      )  # Add graduated_year field
    workplace = ModelChoiceField(queryset=Workplace.objects.all(), required=False)
    position = forms.CharField(required=False)
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'first_name', 'last_name', 'gender', 'dob', 'bio', 'show_contact_info', 
                  'line', 'facebook', 'phone_number', 'email']
        widgets = {'dob': forms.DateInput(attrs={'type': 'date', 'min': '1900-01-01', 'max': datetime.date.today().strftime('%Y-%m-%d')})}
        labels = {'dob': 'Date of Birth', 'email': 'Personal Email'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['dob'] = datetime.date(2000, 1, 1)

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Save additional fields from AlumniProfile
        alumni_profile, _ = AlumniProfile.objects.get_or_create(user_profile=instance)
        alumni_profile.mentor_status = self.cleaned_data['mentor_status']
        alumni_profile.started_year = self.cleaned_data['started_year']  # Save started_year
        alumni_profile.graduated_year = self.cleaned_data['graduated_year'] 
        alumni_profile.workplace = self.cleaned_data['workplace'] 
        alumni_profile.position = self.cleaned_data['position'] 
        # Save graduated_year
        if commit:
            instance.save()
            alumni_profile.save()
        return instance


class CurrentStudentForm(forms.ModelForm):
    current_year = datetime.date.today().year
    profile_picture = forms.FileField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])],required=False)
    mentee_status = forms.BooleanField(required=False, initial=False)  # Adjusted to BooleanField
    started_year = forms.IntegerField(
        min_value=datetime.date.today().year - 8,  # Minimum value 8 years ago
        max_value=datetime.date.today().year,       # Maximum value current year
        label='Started Year',  # Optional label for the field
        required=False,
        initial=datetime.date.today().year-1
    )
    workplace = ModelChoiceField(queryset=Workplace.objects.all(), required=False)
    position = forms.CharField(required=False)
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'first_name', 'last_name', 'gender', 'dob', 'bio', 'show_contact_info', 
                  'line', 'facebook', 'phone_number', 'email']
        widgets = {'dob': forms.DateInput(attrs={'type': 'date', 'min': '1900-01-01', 'max': datetime.date.today().strftime('%Y-%m-%d')}),
                   }
        labels = {'dob': 'Date of Birth', 'email': 'Personal Email'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['dob'] = datetime.date(2000, 1, 1)

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Save additional fields from CurrentStudentProfile
        student_profile, _ = CurrentStudentProfile.objects.get_or_create(user_profile=instance)
        student_profile.mentee_status = self.cleaned_data['mentee_status']
        student_profile.started_year = self.cleaned_data['started_year']
        student_profile.workplace = self.cleaned_data['workplace'] 
        student_profile.position = self.cleaned_data['position'] 
        if commit:
            instance.save()
            student_profile.save()
        return instance

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        
        
        
        
        
        
        
        
        
# class EditForm(forms.ModelForm):
#     current_year = datetime.date.today().year
#     profile_picture = forms.FileField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif'])])
    
    
#     class Meta:
#         model = UserProfile
#         fields = ['profile_picture','first_name', 'last_name', 'gender', 'dob', 'bio', 'show_contact_info', 
#                 'line', 'facebook', 'phone_number', 'email']
#         # Exclude alumni_email and user field from editing (assuming they shouldn't be changed)
#         exclude = ['alumni_email', 'user', 'is_alumni']
#         widgets = {'dob': forms.DateInput(attrs={'type': 'date', 'min': '1900-01-01', 'max': datetime.date.today().strftime('%Y-%m-%d')})}
#         labels = {
#             'dob': 'Date of Birth',
#             'email': 'Personal Email',
#         }
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.initial['dob'] = datetime.date(2000, 1, 1)
    

# class AlumniPrimaryForm(forms.ModelForm):
#     alumni_email = forms.EmailField(
#         validators=[RegexValidator(r'^\d{8}26+@cbs\.alumni$', 'Please use a valid email (format: username@cbs.alumni)')]
#     )
#     student_id = forms.CharField(
#         validators=[RegexValidator(r'^\d{8}26$', 'Student ID must have 10 digits')]
#     )
#     password = forms.CharField(widget=forms.PasswordInput())
#     password_confirmation = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    
#     class Meta:
#         model = AlumniProfile
#         fields = ('first_name', 'last_name','alumni_email','student_id')
        
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password_confirmation = cleaned_data.get("password_confirmation")
#         if len(password) < 8:
#             raise forms.ValidationError("Password must be at least 8 characters long.")
#         if password and password_confirmation and password != password_confirmation:
#             raise forms.ValidationError("Passwords don't match")
#         return cleaned_data
    


# class AlumniPersonalForm(forms.ModelForm):
    # year_choices = [(year, str(year)) for year in range(1930, current_year + 1)]
#     class Meta:
#         current_year = datetime.date.today().year
#         
#         model = AlumniProfile
#         fields = ('profile_picture','dob','gender','started_year','graduated_year','bio','current_position',
#                   'current_workplace','previous_position','previous_workplace','show_contact_info','line',
#                   'facebook','phone_number','email')
#         widgets = {'dob': forms.DateInput(attrs={'type':'date'}),
#                    'started_year': forms.Select(choices=year_choices),
#                    'graduated_year': forms.Select(choices=year_choices),
#                    }
        
        
        
        
# class StudentPrimaryForm(forms.ModelForm):
#     student_email = forms.EmailField(
#         validators=[RegexValidator(r'^\d{8}26+@cbs\.student$', 
#                                    'Please use a valid email (format: username@cbs.student)')]
#     )
#     student_id = forms.CharField(
#         validators=[RegexValidator(r'^\d{10}$', 'Student ID must have 10 digits')]
#     )
#     password = forms.CharField(widget=forms.PasswordInput())
#     password_confirmation = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    
#     class Meta:
#         model = StudentProfile
#         fields = ('first_name', 'last_name','student_email', 'student_id')
    
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password_confirmation = cleaned_data.get("password_confirmation")
#         if len(password) < 8:
#             raise forms.ValidationError("Password must be at least 8 characters long.")
#         if password and password_confirmation and password != password_confirmation:
#             raise forms.ValidationError("Passwords don't match")
#         return cleaned_data

# class StudentPersonalForm(forms.ModelForm):
    
#     class Meta:
#         current_year = datetime.date.today().year
#         year_choices = [(year, str(year)) for year in range(1930, current_year + 1)]
#         model = StudentProfile
#         fields = ('profile_picture','dob','gender','started_year','graduated_year','bio','show_contact_info', 
#                   'internship_position','internship_workplace','line','facebook','phone_number','email',
#                   'grad_high_school')
#         widgets = {'dob': forms.DateInput(attrs={'type':'date'}),
#                    'started_year': forms.Select(choices=year_choices),
#                    'graduated_year': forms.Select(choices=year_choices),
#                    }
        
# class AlumniProfileForm(forms.ModelForm):
#     current_workplace = ModelChoiceField(queryset=Workplace.objects.all(), required=False)
#     previous_workplace = ModelChoiceField(queryset=Workplace.objects.all(), required=False)

#     class Meta:
#         model = AlumniProfile
#         fields = [
#             'alumni_email', 'first_name', 'last_name', 'student_id', 'gender',
#             'dob', 'started_year', 'graduated_year', 'bio', 'current_position',
#             'current_workplace', 'previous_position', 'previous_workplace',
#             'show_contact_info', 'line', 'facebook', 'phone_number', 'email', 'profile_picture'
#         ]
#         widgets = {
#             'dob': forms.DateInput(attrs={'type': 'date'}),
#             'profile_picture': forms.FileInput()
#         }