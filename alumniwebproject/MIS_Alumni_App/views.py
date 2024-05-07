from django.shortcuts import render, redirect, get_object_or_404
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
import datetime
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from itertools import chain
from django.views.decorators.http import require_http_methods

# Create your views here.

def index(request):
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(start_date__gte=today).order_by('start_date')[:2]
    past_events = Event.objects.filter(start_date__lt=today).order_by('-start_date')

    news = News.objects.all().order_by('created')[:6]


    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'news':news
    }
    return render(request, "alumni/index.html", context)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "alumni/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "alumni/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            alumni_email = form.cleaned_data['alumni_email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            confirmation = form.cleaned_data["confirm_password"]
            print(f'{alumni_email}, {first_name},{last_name},{password},{confirmation}')
            try:
                # Create a new user
                user = User.objects.create_user(username=alumni_email, password=password)
                print("User created successfully:", user)
                try:
                    # Create a new user profile
                    user_profile = UserProfile.objects.create(
                        user=user,
                        alumni_email=alumni_email,
                        first_name=first_name,
                        last_name=last_name,
                        is_alumni=True
                    )
                    print("User profile created successfully:", user_profile)
                    try:
                        alumni_profile = AlumniProfile.objects.create(
                            user_profile=user_profile,
                            
                        )
                    except IntegrityError as e:
                        print("Integrity error occurred:", e)
                except IntegrityError as e:
                    print("Integrity error occurred:", e)
                # Authenticate the user
                user = authenticate(request, username=alumni_email, password=password)
                print("Authenticated user:", user)
                if user is not None:
                    # Log in the user
                    login(request, user)
                    print("User logged in successfully")
                    # Redirect to the user's profile page
                    return redirect('profile', user_id=user.id)
                else:
                    # Handle authentication failure
                    return render(request, "alumni/register.html", {
                        "message": "Failed to authenticate user.",
                        'form': form
                    })
            
            except IntegrityError:
                print("error")
                return render(request, "alumni/register.html", {
                "message": "Username already taken.",
                'form': form
                })
        else:
            # Handle invalid form (optional: display errors in the template)
            pass  # Or add logic to display form errors in the template context
    else:
        form = UserRegistrationForm()

    return render(request, 'alumni/register.html', {'form': form})
     

def student_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            alumni_email = form.cleaned_data['alumni_email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            confirmation = form.cleaned_data["confirm_password"]
            print(f'{alumni_email}, {first_name},{last_name},{password},{confirmation}')
            try:
                # Create a new user
                user = User.objects.create_user(username=alumni_email, password=password)
                print("User created successfully:", user)
                try:
                    # Create a new user profile
                    user_profile = UserProfile.objects.create(
                        user=user,
                        alumni_email=alumni_email,
                        first_name=first_name,
                        last_name=last_name,
                        is_alumni=False
                    )
                    print("User profile created successfully:", user_profile)
                    try:
                        student_profile = CurrentStudentProfile.objects.create(
                            user_profile=user_profile,
                        )
                    except IntegrityError as e:
                        print("Integrity error occurred:", e)
                except IntegrityError as e:
                    print("Integrity error occurred:", e)
                # Authenticate the user
                user = authenticate(request, username=alumni_email, password=password)
                print("Authenticated user:", user)
                if user is not None:
                    # Log in the user
                    login(request, user)
                    print("User logged in successfully")
                    # Redirect to the user's profile page
                    return redirect('profile', user_id=user.id)
                else:
                    # Handle authentication failure
                    return render(request, "alumni/student_register.html", {
                        "message": "Failed to authenticate user.",
                        'form': form
                    })
            
            except IntegrityError:
                print("error")
                return render(request, "alumni/student_register.html", {
                "message": "Username already taken.",
                'form': form
                })
        else:
            # Handle invalid form (optional: display errors in the template)
            pass  # Or add logic to display form errors in the template context
    else:
        form = UserRegistrationForm()

    return render(request, 'alumni/student_register.html', {'form': form})

def register_landing(request):
    return render(request,"alumni/landing_register.html")

@login_required
def directory(request):
    query = request.GET.get('q', '')
    user_type = request.GET.get('user_type', '')
    mentorship_status = request.GET.get('mentorship_status', '')

    alumniData = AlumniProfile.objects.select_related('user_profile')
    studentData = CurrentStudentProfile.objects.select_related('user_profile')

    # Filtering based on search query
    if query:
        alumniData = alumniData.filter(
            Q(user_profile__first_name__icontains=query) | 
            Q(user_profile__last_name__icontains=query) |
            Q(workplace__name__icontains=query)
        )
        studentData = studentData.filter(
            Q(user_profile__first_name__icontains=query) | 
            Q(user_profile__last_name__icontains=query) |
            Q(workplace__name__icontains=query)
        )

    # Filtering based on user type
    if user_type == 'alumni':
        studentData = CurrentStudentProfile.objects.none()  # Clear the student data if only alumni selected
    elif user_type == 'student':
        alumniData = AlumniProfile.objects.none()  # Clear the alumni data if only students selected

    if mentorship_status == 'Yes':
        alumniData = alumniData.filter(mentor_status=True)
        studentData = studentData.filter(mentee_status=True)
    elif mentorship_status == 'No':
        alumniData = alumniData.exclude(mentor_status=True)
        studentData = studentData.exclude(mentee_status=True)

    profiles = list(alumniData) + list(studentData)
    paginator = Paginator(profiles, 10)  # Show 10 profiles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'alumnidatas': alumniData,
        'studentdatas': studentData,
        'page_obj' : page_obj
    }
    return render(request, "alumni/directory.html", context)

def event(request):
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(start_date__gte=today).order_by('start_date')
    past_events = Event.objects.filter(start_date__lt=today).order_by('-start_date')
    return render(request, "alumni/events.html", {
        'upcoming_events': upcoming_events,
        'past_events': past_events
    })

def news(request):
    news = News.objects.all()
    return render(request, "alumni/news.html",{
        'news':news
    })


def news_detail(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, "alumni/news_detail.html", {
        'news_item': news_item
    })

def about(request):
    return render(request,'alumni/about.html')

@login_required
def profile(request, user_id):
    request_user = request.user
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(UserProfile, user=user)

    is_editable = request.user == profile.user
     # Check if the user profile is for an alumni
    if profile.is_alumni:
        alumni_user, created = AlumniProfile.objects.get_or_create(user_profile=profile)
        context = {'profile': profile, 'user': user, 'is_editable': is_editable, 'alumni_user': alumni_user, 'request_user':request_user}
        template_name = 'alumni/profile.html'
    else:
        current_student_user, created = CurrentStudentProfile.objects.get_or_create(user_profile=profile)
        context = {'profile': profile, 'user': user, 'is_editable': is_editable, 'current_student_user': current_student_user, 'request_user':request_user}
        template_name = 'alumni/profile.html'

    return render(request, template_name, context)


@login_required
def edit_profile(request, user_id):
    request_user = request.user
    user = get_object_or_404(User, pk=user_id)
    profile = get_object_or_404(UserProfile, user=user)

    # Check if the current user is the same as the profile user
    is_editable = request.user == profile.user

    # Check if the current user is the owner of the profile
    if not is_editable:
        return HttpResponseForbidden("You do not have permission to access this page.")

    initial_data = {}

    # Determine which form class to use based on the profile type
    if profile.is_alumni:
        form_class = AlumniForm
        alumni_profile, _ = AlumniProfile.objects.get_or_create(user_profile=profile)
        initial_data['mentor_status'] = alumni_profile.mentor_status
        initial_data['started_year'] = alumni_profile.started_year
        initial_data['graduated_year'] = alumni_profile.graduated_year
        initial_data['workplace'] = alumni_profile.workplace
        initial_data['position'] = alumni_profile.position
    else:
        form_class = CurrentStudentForm
        current_student_profile, _ = CurrentStudentProfile.objects.get_or_create(user_profile=profile)
        initial_data['mentee_status'] = current_student_profile.mentee_status
        initial_data['started_year'] = current_student_profile.started_year
        initial_data['workplace'] = current_student_profile.workplace
        initial_data['position'] = current_student_profile.position

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            updated_profile = form.save(commit=False)
            updated_profile.user = user  # Ensure the profile is linked to the user
            updated_profile.save()

            # Saving additional fields from AlumniProfile or CurrentStudentProfile
            if profile.is_alumni:
                alumni_profile, created = AlumniProfile.objects.get_or_create(user_profile=profile)
                alumni_profile.mentor_status = form.cleaned_data.get('mentor_status')
                alumni_profile.started_year = form.cleaned_data.get('started_year')
                alumni_profile.graduated_year = form.cleaned_data.get('graduated_year')
                alumni_profile.workplace = form.cleaned_data.get('workplace')
                alumni_profile.position = form.cleaned_data.get('position')
                alumni_profile.save()
            else:
                current_student_profile, created = CurrentStudentProfile.objects.get_or_create(user_profile=profile)
                current_student_profile.mentee_status = form.cleaned_data.get('mentee_status')
                current_student_profile.started_year = form.cleaned_data.get('started_year')
                current_student_profile.workplace = form.cleaned_data.get('workplace')
                current_student_profile.position = form.cleaned_data.get('position')
                current_student_profile.save()

            return redirect('profile', user_id=user_id)  # Redirect to the profile view with user_id
    else:
        form = form_class(instance=profile, initial=initial_data)

    return render(request, 'alumni/editprofile.html', {'form': form, 'profile': profile, 'is_editable': is_editable,'request_user':request_user})

@login_required
def post_list(request):
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # Set the author of the post
            post.author = request.user.userprofile
            post.save()
            return redirect('discussions')  # Redirect to the post_list page
    else:
        form = PostForm()
    
    posts = Post.objects.all()
    return render(request, 'alumni/post_list.html', {'posts': posts, 'form': form})

@login_required
def post_detail(request, pk):
    request_user = request.user
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    
    # Retrieve user, profile, and userprofile
    user = post.author.user
    profile = post.author
    

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user.userprofile
            comment.save()
            # Return JSON response to update comments section via AJAX
            return JsonResponse({
                'success': True, 
                'comment_id': comment.pk, 
                'author': {
                    'username': comment.author.user.username, 
                    'firstname': comment.author.user.first_name
                }, 
                'comment_content': comment.content
            })
        else:
            return JsonResponse({'success': False, 'errors': comment_form.errors})
    else:
        comment_form = CommentForm()
        
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user': user,
        'profile': profile,
    }
    
    return render(request, 'alumni/post_detail.html', context)

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Check if the current user is the author of the post
    if request.user != post.author.user:
        # If not the author, return an error response
        return JsonResponse({'error': 'You are not authorized to edit this post.'}, status=403)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            # If form is not valid, return an error response with form errors
            return JsonResponse({'error': 'Invalid form data.', 'errors': form.errors}, status=400)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'post_detail.html', {'form': form, 'post': post})


@require_http_methods(["DELETE"])
def delete_comment(request, comment_id):
    if request.method == 'DELETE':
        try:
            comment = Comment.objects.get(pk=comment_id)
            # Check if the current user is the author of the comment
            if comment.author.user == request.user:
                comment.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'You are not authorized to delete this comment.'}, status=403)
        except Comment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Comment does not exist.'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)



def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        try:
            post.delete()
            return redirect('discussions')  # Redirect to post list page on success
        except Exception as e:
            # Handle the exception, you can log it or do other actions as needed
            return HttpResponse("Error occurred while deleting the post.")
    return redirect('discussions')  # Redirect to post detail page if not a POST request or deletion was unsuccessful






# class AlumniWizardView(SessionWizardView):
#     form_list = [AlumniPrimaryForm, AlumniPersonalForm]
#     template_name = 'alumni/register.html'
#     file_storage = FileSystemStorage(location='media/alumniPF/')

#     def done(self, form_list, **kwargs):
#         primary_form_data = form_list[0].cleaned_data
#         personal_form_data = form_list[1].cleaned_data
#         username = primary_form_data['alumni_email']
#         password = primary_form_data['password']
        
#         user = User.objects.create_user(username=username, password=password)
       
#         if user:
#             # Create StudentProfile object
#             alumni_profile_data = {
#                 'user': user,
#                 'alumni_email': primary_form_data['alumni_email'],
#                 'student_id': primary_form_data['student_id'],
#                 'first_name': primary_form_data['first_name'],
#                 'last_name': primary_form_data['last_name'],
#                 'profile_picture': personal_form_data['profile_picture'],
#                 'dob': personal_form_data['dob'],
#                 'gender': personal_form_data['gender'],
#                 'started_year': personal_form_data['started_year'],
#                 'graduated_year': personal_form_data['graduated_year'],
#                 'bio': personal_form_data['bio'],
#                 'show_contact_info': personal_form_data['show_contact_info'],
#                 'current_position': personal_form_data['current_position'],
#                 'current_workplace': personal_form_data['current_workplace'],
#                 'line': personal_form_data['line'],
#                 'facebook': personal_form_data['facebook'],
#                 'phone_number': personal_form_data['phone_number'],
#                 'email': personal_form_data['email'],
#                 'previous_position': personal_form_data['previous_position'],
#                 'previous_workplace': personal_form_data['previous_workplace'],
#             }

#             AlumniProfile.objects.create(**alumni_profile_data)

#             # Redirect to login page upon successful registration
#             user = authenticate(username=username, password=password)
#             if user:
#                 login(self.request, user)
#                 return redirect('index')
#             else:
#                 return HttpResponse("Error: Unable to authenticate user")
#         else:
#             # Handle error by redirecting back to registration page
#             return redirect('register')

        
        
        
        
        
# class StudentWizardView(SessionWizardView):
#     form_list = [StudentPrimaryForm, StudentPersonalForm]
#     template_name = 'alumni/student_register.html'
#     file_storage = FileSystemStorage(location='media/studentPF/')
    
#     def done(self, form_list, **kwargs):
#         primary_form_data = form_list[0].cleaned_data
#         personal_form_data = form_list[1].cleaned_data
#         username = primary_form_data['student_email']
#         password = primary_form_data['password']
        
#         # Create User object
#         user = User.objects.create_user(username=username, password=password)

#         if user:
#             # Create StudentProfile object
#             student_profile_data = {
#                 'user': user,
#                 'student_email': primary_form_data['student_email'],
#                 'student_id': primary_form_data['student_id'],
#                 'first_name': primary_form_data['first_name'],
#                 'last_name': primary_form_data['last_name'],
#                 'profile_picture': personal_form_data['profile_picture'],
#                 'dob': personal_form_data['dob'],
#                 'gender': personal_form_data['gender'],
#                 'started_year': personal_form_data['started_year'],
#                 'graduated_year': personal_form_data['graduated_year'],
#                 'bio': personal_form_data['bio'],
#                 'show_contact_info': personal_form_data['show_contact_info'],
#                 'internship_position': personal_form_data['internship_position'],
#                 'internship_workplace': personal_form_data['internship_workplace'],
#                 'line': personal_form_data['line'],
#                 'facebook': personal_form_data['facebook'],
#                 'phone_number': personal_form_data['phone_number'],
#                 'email': personal_form_data['email'],
#                 'grad_high_school': personal_form_data['grad_high_school'],
#             }

#             StudentProfile.objects.create(**student_profile_data)

#             # Redirect to login page upon successful registration
#             user = authenticate(username=username, password=password)
#             if user:
#                 login(self.request, user)
#                 return redirect('index')
#             else:
#                 return HttpResponse("Error: Unable to authenticate user")
#         else:
#             # Handle error by redirecting back to registration page
#             return redirect('student_register')
