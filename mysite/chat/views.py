from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ChatSocketInfoView(APIView):
    """
    WebSocket-инструкция для подключения к чату
    """

    @swagger_auto_schema(
        operation_description="""
        ## 🔌 WebSocket API: Подключение к чату

        URL подключения:
        ws://127.0.0.1:8000/ws/chat/general/?token=

        Формат сообщений: JSON.
        """
    )
    def post(self, request):
        data = {
            "message": "Для подключения используйте /ws/chat/general/?token= с JSON-сообщениями"
        }
        return Response(data, status=status.HTTP_200_OK)
