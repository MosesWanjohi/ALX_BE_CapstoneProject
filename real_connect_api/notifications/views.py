from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

class MarkNotificationAsReadView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, *args, **kwargs):
        notification = self.get_object()
        if notification.recipient != request.user:
            return Response({'message': 'You cannot mark this notification'}, status=status.HTTP_403_FORBIDDEN)

        notification.is_read = True
        notification.save()
        return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)
