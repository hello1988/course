from django.contrib import admin

from .models import Member
from .models import Course
from .models import CourseSchedule
from .models import CourseApply
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_name',)
    search_fields = ('display_name',)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

class CourseScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'start_date',)
    list_filter = ('course',)

class CourseApplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'schedule',)
    list_filter = ('schedule',)
    search_fields = ('member__name', 'member__display_name',)

admin.site.register(Member, MemberAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseSchedule, CourseScheduleAdmin)
admin.site.register(CourseApply, CourseApplyAdmin)
