from django.urls import path
from .views import ChatSocketInfoView

urlpatterns = [
    path("ws_doc/", ChatSocketInfoView.as_view(), name="ws_doc"),
]
