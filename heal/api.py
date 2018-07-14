# from .repos import member_repo
from .services import course_schedule_service
from .services import course_apply_service

def process_text_message(line_id, message_text):
    # 關鍵字處理
    if message_text == '#近期課程':
        course_schedule_service.push_recent_course(line_id)

    elif message_text == '#我的課程':
        course_apply_service.push_my_recent_courses(line_id)

    # 問答處理

    # 預設訊息

def process_postback(line_id, postback_text):

    # 近期課程
    if postback_text == 'COURSE_QUERY':
        course_schedule_service.push_recent_course(line_id)

    # 報名課程
    elif postback_text.startswith('COURSE_APPLY'):
        course_schedule_id = int( postback_text.replace('COURSE_APPLY#', '') )
        course_apply_service.apply_course(line_id, course_schedule_id)

        course_apply_service.push_my_recent_courses(line_id)