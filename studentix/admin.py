from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Course
from .models import LoginUser
from .models import CourseContent
from .models import Quiz
from .models import Question


from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



class MyAdminSite(AdminSite):
    site_header = 'STUDENTIX'
    AdminSite.index_title = 'STUDENTIX SITE ADMINISTRATION'



class LoginUserline(admin.StackedInline):
    model = LoginUser
    can_delete = False
    verbose_name_plural = 'LoginUser'
    empty_value_display = '-empty-'


class CourseContentline(admin.StackedInline):
    model = CourseContent
    can_delete = False
    verbose_name_plural = 'CourseContent'
    empty_value_display = '-empty-'


class Quizline(admin.StackedInline):
    model = Quiz
    can_delete = False
    verbose_name_plural = 'Quiz'
    empty_value_display = '-empty-'


class Questionline(admin.StackedInline):
    model = Question
    can_delete = False
    verbose_name_plural = 'Question'
    empty_value_display = '-empty-'


class UserAdmin(BaseUserAdmin):
    inlines = (LoginUserline,)




class LoginUserAdmin(admin.ModelAdmin):
    
    save_on_top = True
    search_fields = ['user__username']
    fieldsets = [
        (None,               {'fields': ['user']}),
        (None,               {'fields': ['contactNo']}),
        (None,               {'fields': ['dob']}),
        (None,               {'fields': ['type']}),
    ]
    list_display = ('user','contactNo', 'dob', 'type',)
    list_filter = ['type']
    ordering = ['user']
    date_hierarchy = 'dob'
    empty_value_display = '-empty-'


class QuestionAdmin(admin.ModelAdmin):
    
    save_on_top = True
    search_fields = ['Question']
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        (None,               {'fields': ['choice_1']}),
        (None,               {'fields': ['choice_2']}),
        (None,               {'fields': ['choice_3']}),
        (None,               {'fields': ['choice_4']}),
        (None,               {'fields': ['answer']}),
    ]
    list_display = ('question_text','choice_1', 'choice_2', 'choice_3', 'choice_4', 'answer',)
    empty_value_display = '-empty-'




class QuizAdmin(admin.ModelAdmin):
    
    save_on_top = True
    empty_value_display = '-empty-'
    # inlines = (Questionline,)


class CourseContentAdmin(admin.ModelAdmin):
    
    save_on_top = True
    search_fields = ['CourseContent']
    fieldsets = [
        (None,               {'fields': ['title']}),
        (None,               {'fields': ['content']}),
    ]

    list_display = ('title', 'content',)
    
    empty_value_display = '-empty-'




class CourseAdmin(admin.ModelAdmin):
    
    save_on_top = True
    search_fields = ['courseName']
    fieldsets = [
        (None,               {'fields': ['courseName']}),
        (None,               {'fields': ['description']}),
        (None,               {'fields': ['prerequisites']}),
        (None,               {'fields': ['payments']}),
        (None,               {'fields': ['syllabus']}),
        (None,               {'fields': ['image']}),
        (None,               {'fields': ['status']}),
        (None,               {'fields': ['mid_term']}),
        (None,               {'fields': ['end_term']}),
    ]
    list_display = ('courseName','description' ,'prerequisites', 'payments','syllabus','image','status','mid_term','end_term',)
    list_filter = ['payments']
    ordering = ['courseName']
    empty_value_display = '-empty-'
    inlines = (Quizline,Questionline,)


admin_site = MyAdminSite(name='admin')
admin_site.empty_value_display = '(None)'


# admin_site.unregister(User)
# admin_site.unregister(Group)
admin_site.register(User, UserAdmin)

admin_site.register(Course,CourseAdmin)
admin_site.register(LoginUser,LoginUserAdmin)
admin_site.register(Quiz, QuizAdmin)
admin_site.register(CourseContent)
# admin_site.register(Question)