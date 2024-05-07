from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(AlumniProfile)
admin.site.register(CurrentStudentProfile)
admin.site.register(Workplace)
admin.site.register(UserProfile)
admin.site.register(News)
admin.site.register(Event)
admin.site.register(Post)
admin.site.register(Comment)