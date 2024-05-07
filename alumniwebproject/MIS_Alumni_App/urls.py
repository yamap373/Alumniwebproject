from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("student_register", views.student_register, name="student_register"),
    path("directory", views.directory, name="directory"),
    path("event",views.event,name="event"),
    path("news", views.news, name="news"),
    path("register_landing", views.register_landing, name="register_landing"),
    path("directory/profile/<int:user_id>", views.profile, name="profile"),
    path('edit-profile/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path("news/<int:news_id>/", views.news_detail, name="news_detail"),
    path("about",views.about, name="about"),
    path("discussions",views.post_list, name="discussions"),
    path("discussions/post_detail/<int:pk>/",views.post_detail, name="post_detail"),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('delete-post/<int:pk>/', views.delete_post, name='delete_post'),
    path('edit-post/<int:pk>/', views.edit_post, name='edit_post'),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)