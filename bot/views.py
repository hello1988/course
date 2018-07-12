from django.conf import settings
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from linebot import WebhookHandler
from linebot.models import MessageEvent, TextMessage, PostbackEvent, FollowEvent

handler = WebhookHandler(settings.CHANNEL_SECRET)

class LineBotViewSet(ViewSet):

    @action(methods=['post'], detail=False, url_path='webhook')
    def webhook(self, request):
        # get X-Line-Signature header value
        signature = request.META.get('HTTP_X_LINE_SIGNATURE')
        # get request body as text
        body = request.body.decode('utf-8')
        try:
            handler.handle(body, signature)
        except Exception as e:
            print(str(e))

        return HttpResponse()

    @handler.add(FollowEvent)
    def handle_follow(event, *args, **kwargs):
        # self = event
        print(event)

    @handler.add(MessageEvent, message=TextMessage)
    def handle_text_message(event, *args, **kwargs):
        line_id = event.source.user_id
        reply_token = event.reply_token
        text = event.message.text


    @handler.add(PostbackEvent)
    def handle_postback(event, *args, **kwargs):
        # self = event
        print(args)
        print(kwargs)