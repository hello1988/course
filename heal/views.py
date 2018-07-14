from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from bot.utils import push_templates

from .services import member_service

from linebot.models import TextSendMessage
# Create your views here.

class MemberViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    @action(methods=['get', 'post'], detail=False, url_path='registered')
    def registered(self, request):
        if request.method == 'GET':
            return render( request, 'registered.html' )

        elif request.method == 'POST':
            data = dict(request.data)
            # print(data)
            line_id = data.get('line_id')
            name = data.get('name')

            member_service.modify(line_id, name, registered=True)

            text = '恭喜你 {name} 註冊成功囉'.format(name=name)
            push_templates(line_id, TextSendMessage(text=text))

        return HttpResponse()