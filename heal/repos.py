import time
from linebot import LineBotApi
from django.conf import settings
from .models import Member
from .models import CourseSchedule
from .models import CourseApply

line_bot_api = LineBotApi( settings.CHANNEL_TOKEN )
class MemberRepo(object):
    def get_by_line_id(self, line_id):
        member, created = Member.objects.get_or_create(line_id=line_id)
        if created:
            profile = line_bot_api.get_profile(line_id)
            member.name = profile.display_name
            member.display_name = ''
            member.save()

        return member

class CourseScheduleRepo(object):
    def get_recent_courses(self):
        now = int(time.time())
        course_schedules = CourseSchedule.objects.filter(start_time__gte=now).order_by('start_date')

        schedules = {}
        courses = {}
        for schedule in course_schedules:
            course = schedule.course
            if course.id not in schedules:
                schedules[course.id] = []
                courses[course.id] = course

            if len(schedules[course.id]) >= 2:
                continue

            schedules[course.id].append(schedule)

        return schedules, courses

class CourseApplyRepo(object):
    def apply(self, member, schedule_id):
        CourseApply.objects.get_or_create(schedule_id=schedule_id, member=member)

    def get_my_recent_courses(self, member):
        now = int(time.time())
        courses = CourseApply.objects.filter(member=member, schedule__start_time__gte=now).order_by('schedule__start_time')
        return courses


member_repo = MemberRepo()
course_schedule_repo = CourseScheduleRepo()
course_apply_repo = CourseApplyRepo()