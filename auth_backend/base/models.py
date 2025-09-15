from django.db import models
import uuid
import os
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


def user_profile_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}_{uuid.uuid4().hex}.{ext}"
    return os.path.join('user_profiles', filename)


# Create your models here.
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_image = models.ImageField(upload_to=user_profile_upload_path, null=True, blank=True)
    
    twofa_enabled = models.BooleanField(default=False, blank=True, null=True)
    totp_secret = models.CharField(max_length=256, blank=True, null=True)
    
    immich_email = models.EmailField(null=True, blank=True)
    immich_password = models.CharField(max_length=128, null=True, blank=True) 
    immich_pat = models.CharField(max_length=128, null=True, blank=True)
    immich_entry_album_id = models.UUIDField(blank=True, null=True)

    
    
class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='notes',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Calendar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owned_calendars")
    shared_users = models.ManyToManyField(CustomUser, through="CalendarShare", related_name="shared_calendars")
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class CalendarShare(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    shared_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("calendar", "shared_user")
        
        
class CalendarEvent(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="calendar_events")
    date = models.DateField()
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name="events", null=False)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_all_day = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    location = models.CharField(max_length=255, null=True, blank=True)
    tags = models.JSONField(default=list, null=True, blank=True)
    urls = models.JSONField(default=list, null=True, blank=True)
    checklist = models.JSONField(default=list, null=True, blank=True)
    is_public = models.BooleanField(default=False)
    notification_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def clean(self):
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("開始時刻は終了時刻より前でなければなりません")

    

class DiaryBook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owned_books")
    shared_users = models.ManyToManyField(
        CustomUser,
        through="DiaryBookShare",
        related_name="shared_books"
    )
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
    
class DiaryBookShare(models.Model):
    book = models.ForeignKey(DiaryBook, on_delete=models.CASCADE)
    shared_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("book", "shared_user")
        
        

    
class Entry(models.Model):
    class EntryStatus(models.TextChoices):
        DRAFT = "draft", _("下書き")
        COMPLETE = "complete", _("完了")
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    book = models.ForeignKey(DiaryBook, on_delete=models.CASCADE, related_name="entries",null=False)
    title = models.CharField(max_length=128)
    author = models.ForeignKey(CustomUser, related_name='entries', on_delete=models.CASCADE)
    body = models.TextField()
    entry_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        choices=EntryStatus.choices,
        default=EntryStatus.DRAFT,
        max_length=10
    )
    tags = models.JSONField(default=list, blank=True)
    is_public = models.BooleanField(default=False)
    shared_users = models.ManyToManyField(
        CustomUser,
        through="EntryShare",
        through_fields=('entry', 'shared_user'),
        related_name="shared_entries"
    )
    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'], name='unique_entry_per_author')
        ]
        verbose_name = _("Entry")
        verbose_name_plural = _("Entries List")
        
    def __str__(self):
        return self.title
    
def user_directory_path(instance, filename):
    # 例: entry_files/<owner_id>/<filename>
    # return f'entry_files/{instance.owner.id}/{filename}'
    return f'entry_files/{instance.entry.author.id}/{filename}'


    
class EntryImages(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(CustomUser, related_name='images', on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, related_name='images', on_delete=models.CASCADE)
    immich_asset_id = models.CharField(max_length=64,null=True,blank=True,)  # ID from Immich
    
    
class EntryShare(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="shared_with")
    shared_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("entry", "shared_user")
    
    def __str__(self):
        return f"{self.shared_user.username} {'can edit' if self.can_edit else 'can view'} '{self.entry.title}'"
    
    
class ReminderGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owned_reminder_groups")
    shared_users = models.ManyToManyField(CustomUser, through="ReminderGroupShare", related_name="shared_reminder_groups")
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class ReminderGroupShare(models.Model):
    group = models.ForeignKey(ReminderGroup, on_delete=models.CASCADE)
    shared_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("group", "shared_user")

    
    
class Reminder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reminders')
    group = models.ForeignKey(ReminderGroup, on_delete=models.CASCADE, related_name="reminders")
    title = models.CharField(max_length=128)
    due_date = models.DateField(blank=True)
    is_public = models.BooleanField(default=False)
    notification_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title} ({self.due_date})"
    
    def save(self, *args, **kwargs):
        self.user = self.group.owner  # 一貫性を保つ
        super().save(*args, **kwargs)
    