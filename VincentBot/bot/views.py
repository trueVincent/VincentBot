from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
import os

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, FlexSendMessage, PostbackEvent

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


class IndexView(View):
    template_name = 'bot/index.html'

    def get(self, request):
        return render(request, self.template_name)


# 回傳使用者傳來的訊息
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        reply = TextSendMessage(text='Hello, World!')
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                receive_message = event.message.text
                # user_id = event.source.user_id

                if receive_message == '個人檔案':
                    flex_message = json.load(open('bot/static/json/profile.json', 'r', encoding='utf-8'))
                    reply = FlexSendMessage('profile', flex_message)
                elif receive_message == '專案經歷':
                    flex_message = json.load(open('bot/static/json/portfolio.json', 'r', encoding='utf-8'))
                    reply = FlexSendMessage('portfolio', flex_message)
                elif receive_message == '社團經歷':
                    flex_message = json.load(open('bot/static/json/club.json', 'r', encoding='utf-8'))
                    reply = FlexSendMessage('club', flex_message)
                elif receive_message == '動機':
                    flex_message = json.load(open('bot/static/json/motivation.json', 'r', encoding='utf-8'))
                    reply = FlexSendMessage('club', flex_message)
                elif receive_message == '技能':
                    flex_message = json.load(open('bot/static/json/skills.json', 'r', encoding='utf-8'))
                    reply = FlexSendMessage('club', flex_message)
                elif receive_message == '興趣':
                    flex_message = json.load(open('bot/static/json/interests.json', 'r', encoding='utf-8'))
                    reply = FlexSendMessage('club', flex_message)

            elif isinstance(event, PostbackEvent):
                receive_message = event.postback.data
                if receive_message == 'Club Meetings':
                    flex_message = json.load(open('bot/static/json/club/club_meetings.json', 'r', encoding='utf-8'))
                    reply = FlexSendMessage('club', flex_message)
                elif receive_message == 'Summer Joint Study Group':
                    flex_message = json.load(open('bot/static/json/club/summer_joint_study_group.json', 'r', encoding='utf-8'))
                    reply = FlexSendMessage('club', flex_message)
                elif receive_message == 'Joint Meeting':
                    flex_message = json.load(open('bot/static/json/club/joint_meeting.json', 'r', encoding='utf-8'))
                    reply = FlexSendMessage('club', flex_message)
                elif receive_message == 'Club Events':
                    flex_message = json.load(open('bot/static/json/club/club_events.json', 'r', encoding='utf-8'))
                    reply = FlexSendMessage('club', flex_message)
                elif receive_message == 'motor photos':
                    flex_message = json.load(open('bot/static/json/interests/motorcycle.json', 'r', encoding='utf-8'))
                    reply = FlexSendMessage('club', flex_message)
                elif receive_message == 'music photos':
                    flex_message = json.load(open('bot/static/json/interests/music.json', 'r', encoding='utf-8'))
                    reply = FlexSendMessage('club', flex_message)
                elif receive_message == 'travel photos':
                    flex_message = json.load(open('bot/static/json/interests/travel.json', 'r', encoding='utf-8'))
                    reply = FlexSendMessage('club', flex_message)

            if reply:
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    reply
                )

        return HttpResponse()
    else:
        return HttpResponseBadRequest()
