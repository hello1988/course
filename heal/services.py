from math import ceil
from .repos import member_repo
from .repos import course_schedule_repo
from .repos import course_apply_repo

from bot.utils import push_templates
from linebot.models import (
    TemplateSendMessage, CarouselTemplate, CarouselColumn,
    PostbackAction, MessageAction,
)

class MemberService(object):

    def modify(self, line_id, name, registered=None):
        member = member_repo.get_by_line_id(line_id)
        if not member:
            return

        member.display_name = name
        member.save()

    def is_registered(self, line_id):
        member = member_repo.get_by_line_id(line_id)
        return bool(member.display_name)

class CourseScheduleService(object):

    def push_recent_course(self, line_id):
        # member = member_repo.get_by_line_id(line_id)
        schedules, courses = course_schedule_repo.get_recent_courses()

        columns = []
        for course_id, schedule in schedules.items():
            course = courses[course_id]
            actions = []

            actions.append(MessageAction(label='課程說明', text=course.description))
            for course_schedule in schedule:
                label = course_schedule.start_date
                data = 'COURSE_APPLY#{}'.format(course_schedule.id)
                actions.append( PostbackAction(label=label, data=data, display_text='報名資料已送出') )

            empty_count = 3-len(actions)
            for i in range(empty_count):
                actions.append(PostbackAction(label='-', data=' '))

            col = CarouselColumn(title=course.name, text=course.desc, actions=actions,
                thumbnail_image_url=course.image_url)
            columns.append(col)

        loop_count = int( ceil( len(columns)/10 ) )
        templates = []
        for i in range(loop_count):
            template = TemplateSendMessage(
                alt_text='近期課程來囉',
                template= CarouselTemplate( columns=columns[ i*10:(i+1)*10 ], image_aspect_ratio='square' ),
            )
            templates.append(template)

        push_templates(line_id, templates)

class CourseApplyService(object):
    def apply_course(self, line_id, schedule_id):
        member = member_repo.get_by_line_id(line_id)
        course_apply_repo.apply(member, schedule_id)

    def push_my_recent_courses(self, line_id):
        member = member_repo.get_by_line_id(line_id)
        applied_courses = course_apply_repo.get_my_recent_courses(member)[:10]

        columns = []
        for applied_course in applied_courses:
            schedule = applied_course.schedule
            course = schedule.course

            actions = []
            actions.append(MessageAction(label='課程說明', text=course.description))

            title = '{name}  {start}'.format(name=course.name, start=schedule.start_date)
            col = CarouselColumn(title=title, text=course.desc, actions=actions,
                thumbnail_image_url=course.image_url)
            columns.append(col)

        template = TemplateSendMessage(
            alt_text='近期課程來囉',
            template=CarouselTemplate(columns=columns, image_aspect_ratio='square'),
        )

        push_templates(line_id, [template])

member_service = MemberService()
course_schedule_service = CourseScheduleService()
course_apply_service = CourseApplyService()