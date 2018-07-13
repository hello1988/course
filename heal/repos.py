from linebot import LineBotApi
from django.conf import settings
from .models import Member

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

member_repo = MemberRepo()