from .repos import member_repo

def process_text_message(line_id, message_text):
    member = member_repo.get_by_line_id(line_id)

def process_postback(line_id, postback_text):
    member = member_repo.get_by_line_id(line_id)