
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from base import views

router = DefaultRouter()

# User and Auth
router.register(r'users', views.CustomUserViewSet)
router.register(r'notes', views.NoteViewSet)

# Calendar
router.register(r'calendars', views.CalendarViewSet)
router.register(r'calendar-events', views.CalendarEventViewSet)
router.register(r'calendar-shares', views.CalendarShareViewSet)

# Diary
router.register(r'diary-books', views.DiaryBookViewSet)
router.register(r'diary-entries', views.EntryViewSet)
router.register(r'diary-book-shares', views.DiaryBookShareViewSet)
router.register(r'diary-entry-images', views.EntryImagesViewSet)
router.register(r'diary-entry-shares', views.EntryShareViewSet)

# Reminder
router.register(r'reminder-groups', views.ReminderGroupViewSet)
router.register(r'reminders', views.ReminderViewSet)
router.register(r'reminder-group-shares', views.ReminderGroupShareViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
