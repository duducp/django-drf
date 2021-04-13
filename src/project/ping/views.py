from django.utils import timezone

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from project import __version__


class PingView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, format=None):
        data = {
            'message': 'pong',
            'version': __version__,
            'datetime': timezone.now().isoformat()
        }

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
