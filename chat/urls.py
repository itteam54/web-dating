from django.urls import path, include
from . import views #chat, new_message_check, wink, chat_ajax, chat_home, read_messages, winks, read_wink, read_view, views, reject

urlpatterns = [
    path('home/', views.chat_home, name="chat_home"),
    path('<id>/', views.chat, name="chat"),
    path('wink/<id>', views.wink, name="wink"),
    path('winks/<id>', views.winks, name="winks"),
    path('views/<id>', views.views, name="views"),
]
