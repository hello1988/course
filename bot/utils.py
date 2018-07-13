from django.conf import settings
from linebot import LineBotApi

line_bot_api = LineBotApi(settings.CHANNEL_TOKEN)

def push_templates(line_id, templates):
    line_bot_api.push_message(line_id, templates)