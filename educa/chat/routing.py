from django.urls import re_path
from . import consumers

# ws/ -> dobra praktyka dla oznaczania websocket url
websocket_urlpatterns = [
    re_path(r'ws/chat/room/(?P<course_id>\d+)/$', consumers.ChatConsumer)
]