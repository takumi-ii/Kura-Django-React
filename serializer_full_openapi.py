from rest_framework import serializers
from base.models import (
    CustomUser, Note, Calendar, CalendarEvent, DiaryBook, DiaryBookShare,
    Entry, EntryImages, EntryShare, ReminderGroup, ReminderGroupShare, Reminder
)

# ----------------------------
# ユーザー
# ----------------------------
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "first_name", "last_name", "profile_image", "twofa_enabled", "last_login")

class PasswdUpdateSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()


# ----------------------------
# ノート
# ----------------------------
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)


# ----------------------------
# カレンダー
# ----------------------------
class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = "__all__"

class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = "__all__"

    def create(self, validated_data):
        validated_data["calendar"] = self.context["request"].user.default_calendar
        return super().create(validated_data)


# ----------------------------
# 日記帳・日記エントリ
# ----------------------------
class DiaryBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryBook
        fields = "__all__"

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = "__all__"

    def create(self, validated_data):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data)

class EntryShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryShare
        fields = "__all__"

class EntryImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryImages
        fields = "__all__"


# ----------------------------
# リマインダー
# ----------------------------
class ReminderGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReminderGroup
        fields = "__all__"

    def create(self, validated_data):
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)

class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = "__all__"

    def create(self, validated_data):
        validated_data["user"] = validated_data["group"].owner
        return super().create(validated_data)
