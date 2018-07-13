from django.conf import settings
from django.http import HttpResponse
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from linebot import WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage, PostbackEvent, FollowEvent,
    TextSendMessage,TemplateSendMessage, ButtonsTemplate,
    URIAction, PostbackAction,
)
from .utils import push_templates

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
        line_id = event.source.user_id
        reply_token = event.reply_token

        text = '歡迎加入這支測試bot，請先完成基本資料的輸入，就可以開始報名課程囉'
        text = TextSendMessage(text=text)

        btn = ButtonsTemplate(
            text='我們需要知道如何稱呼你\n請點擊下方的按鈕開始輸入',
            actions=[
                URIAction(label='開始註冊', uri=settings.LIFF_URL)
            ]
        )

        btn_tpl = TemplateSendMessage( template=btn, alt_text='歡迎加入這支測試bot' )
        push_templates( line_id, [text, btn_tpl] )

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