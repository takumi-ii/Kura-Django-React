
from rest_framework import viewsets, permissions
from .models import (
    CustomUser, Note, Calendar, CalendarShare, CalendarEvent,
    DiaryBook, DiaryBookShare, Entry, EntryImages, EntryShare,
    ReminderGroup, ReminderGroupShare, Reminder
)
from .serializer import (
    CustomUserSerializer, NoteSerializer, CalendarSerializer,
    CalendarShareSerializer, CalendarEventSerializer,
    DiaryBookSerializer, DiaryBookShareSerializer, EntrySerializer,
    EntryImagesSerializer, EntryShareSerializer,
    ReminderGroupSerializer, ReminderGroupShareSerializer,
    ReminderSerializer
)

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    permission_classes = [permissions.IsAuthenticated]

class CalendarShareViewSet(viewsets.ModelViewSet):
    queryset = CalendarShare.objects.all()
    serializer_class = CalendarShareSerializer
    permission_classes = [permissions.IsAuthenticated]

class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    permission_classes = [permissions.IsAuthenticated]

class DiaryBookViewSet(viewsets.ModelViewSet):
    queryset = DiaryBook.objects.all()
    serializer_class = DiaryBookSerializer
    permission_classes = [permissions.IsAuthenticated]

class DiaryBookShareViewSet(viewsets.ModelViewSet):
    queryset = DiaryBookShare.objects.all()
    serializer_class = DiaryBookShareSerializer
    permission_classes = [permissions.IsAuthenticated]

class EntryViewSet(viewsets.ModelViewSet):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [permissions.IsAuthenticated]

class EntryImagesViewSet(viewsets.ModelViewSet):
    queryset = EntryImages.objects.all()
    serializer_class = EntryImagesSerializer
    permission_classes = [permissions.IsAuthenticated]

class EntryShareViewSet(viewsets.ModelViewSet):
    queryset = EntryShare.objects.all()
    serializer_class = EntryShareSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReminderGroupViewSet(viewsets.ModelViewSet):
    queryset = ReminderGroup.objects.all()
    serializer_class = ReminderGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReminderGroupShareViewSet(viewsets.ModelViewSet):
    queryset = ReminderGroupShare.objects.all()
    serializer_class = ReminderGroupShareSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]
