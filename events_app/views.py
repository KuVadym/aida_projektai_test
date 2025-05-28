from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import Events
from .filters import EventFilter
from .serializers import PublicEventsSerializer, MyEventsSerializer
from .utils import send_registration_email


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Events.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = EventFilter
    search_fields = ['title', 'description']
    ordering_fields = ['date', 'title']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()

        # Optional: Add creator as attendee automatically
        event.attendees.add(request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        if self.action == 'my_events':
            return self.request.user.registered_events.all()
        return Events.objects.all()

    def get_serializer_class(self):
        if self.action == 'my_events':
            return MyEventsSerializer
        return PublicEventsSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()
        user = request.user

        if user in event.attendees.all():
            return Response({'detail': 'Ви вже зареєстровані на цю подію.'}, status=status.HTTP_400_BAD_REQUEST)

        event.attendees.add(user)

        send_registration_email(user, event)

        return Response({'detail': 'Реєстрація пройшла успішно.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def my_events(self, request):
        events = request.user.registered_events.all()
        filtered_qs = EventFilter(request.GET, queryset=events).qs
        serializer = MyEventsSerializer(filtered_qs, many=True, context={'request': request})
        return Response(serializer.data)
    