from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.
class User(AbstractUser):
    pass

class Workplace(models.Model):
    name = models.CharField(max_length=100)
    location = models.TextField(blank= True)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alumni_email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_alumni = models.BooleanField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Undefined'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    show_contact_info = models.BooleanField(default=False,null=True)
    line = models.CharField(max_length=100, blank=True, null=True)
    facebook = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='ProfileUserPF/', blank=True, null=True)
    

    REQUIRED_FIELDS = ['first_name', 'last_name', 'alumni_email','user','is_alumni']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class AlumniProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    mentor_status = models.BooleanField(null=True,default=False)
    started_year = models.IntegerField(null=True, blank=True)
    graduated_year = models.IntegerField(null=True, blank=True)
    workplace = models.ForeignKey(Workplace, null=True, blank=True, on_delete=models.CASCADE, related_name="current_employee")
    position = models.CharField(max_length=255, null=True, blank=True)
    previous_workplace = models.ForeignKey(Workplace, null=True, blank=True, on_delete=models.CASCADE,related_name="former_employee")
    previous_position = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user_profile.first_name} {self.user_profile.last_name}"


class CurrentStudentProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    mentee_status = models.BooleanField(null=True,default=False)
    started_year = models.IntegerField(null=True, blank=True)
    workplace = models.ForeignKey(Workplace, null=True, blank=True, on_delete=models.CASCADE)
    position = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user_profile.first_name} {self.user_profile.last_name}"

    
class Event(models.Model):
    title = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255, null=True)
    venue = models.CharField(max_length=255, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    main_picture = models.ImageField(upload_to='EventMain/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.title} starts at {self.start_date} ends at{self.end_date}"
    
class News(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    main_picture = models.ImageField(upload_to='NewsMain/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.title}"
    
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.title} by {self.author}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.post} commented by {self.author}"