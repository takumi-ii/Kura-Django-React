from django.contrib import admin
from .models import Note, CustomUser, CalendarEvent, Entry, Calendar, CalendarShare, EntryImages, EntryShare, Reminder, ReminderGroup, ReminderGroupShare


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Note)
admin.site.register(CalendarEvent)
admin.site.register(Calendar)
admin.site.register(CalendarShare)
admin.site.register(EntryImages)
admin.site.register(EntryShare)
admin.site.register(Reminder)
admin.site.register(ReminderGroup)
admin.site.register(ReminderGroupShare)