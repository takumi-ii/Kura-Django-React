from rest_framework import serializers
from .models import Note, CustomUser, CalendarEvent, EntryImages, Entry


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username']
        
        
class UserGetSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    calendar_ids = serializers.SerializerMethodField()
    diarybook_ids = serializers.SerializerMethodField()
    reminder_group_ids = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'last_login',
            'first_name', 'last_name', 'twofa_enabled',
            'profile_image',
            'calendar_ids',
            'diarybook_ids',
            'reminder_group_ids',
        ]

    def get_profile_image(self, obj):
        request = self.context.get('request')
        if obj.profile_image and hasattr(obj.profile_image, 'url'):
            return request.build_absolute_uri(obj.profile_image.url)
        return None

    def get_calendar_ids(self, obj):
        return [
            {"id": str(cal.id), "name": cal.name}
            for cal in obj.owned_calendars.all()
        ]

    def get_diarybook_ids(self, obj):
        return [
            {"id": str(book.id), "name": book.name}
            for book in obj.owned_books.all()
        ]

    def get_reminder_group_ids(self, obj):
        return [
            {"id": str(group.id), "name": group.name}
            for group in obj.owned_reminder_groups.all()
        ]
    

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'profile_image']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'profile_image': {'required': False},
        }
        
        def get_profile_image(self, obj):
            request = self.context.get('request')
            if obj.profile_image and hasattr(obj.profile_image, 'url'):
                return request.build_absolute_uri(obj.profile_image.url)
            return None
        


class PasswdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
            instance.save()
        return instance
    
    
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'description', 'owner']


class EntryNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['description']
        
    def create(self, validated_data):
        # 現在のユーザーを context から取得（view で context={'request': request} を渡す必要あり）
        user = self.context['request'].user
        return Note.objects.create(owner=user, **validated_data)
    
class CalendarEventSerializer(serializers.ModelSerializer):
    event_id = serializers.UUIDField()

    class Meta:
        model = CalendarEvent
        fields = '__all__'    
        
        
class CalendarEventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        exclude = ['event_id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        # ユーザーはリクエストから取得
        user = self.context['request'].user
        return CalendarEvent.objects.create(user=user, **validated_data)
    
    
class CalendarEventUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        exclude = ['event_id', 'user', 'created_at', 'updated_at']


class EntryImageSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = EntryImages
        fields = ['id', 'immich_asset_id', 'thumbnail_url']

    def get_thumbnail_url(self, obj):
        return f"http://192.168.0.11:2283/api/assets/{obj.immich_asset_id}/thumbnail"
    
    
class EntryDetailSerializer(serializers.ModelSerializer):
    images = EntryImageSerializer(many=True)

    class Meta:
        model = Entry
        fields = ['id', 'title', 'body', 'images', 'entry_date']
        
        
class ImmichPATUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['immich_pat']
        extra_kwargs = {'immich_pat': {'write_only': True}}
        
        
class EntryImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntryImages
        fields = ['id', 'immich_asset_id']
        
        
class EntrySerializer(serializers.ModelSerializer):
    images = EntryImagesSerializer(many=True, read_only=True)
    class Meta:
        model = Entry
        fields = '__all__'
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'entry_date']

