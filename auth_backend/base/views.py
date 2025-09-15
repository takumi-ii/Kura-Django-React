from .models import Note, CalendarEvent, Entry, EntryImages, DiaryBook
from .serializer import (
    NoteSerializer, 
    UserRegisterSerializer, 
    UserGetSerializer, 
    PasswdUpdateSerializer, 
    EntryNoteSerializer, 
    CalendarEventSerializer, 
    CalendarEventCreateSerializer,
    CalendarEventUpdateSerializer,
    ProfileUpdateSerializer,
    EntrySerializer,
    EntryImagesSerializer,
    )
from rest_framework import generics, filters
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse
from .weather_service import get_weather_info, get_address_from_latlng
from .immich import *
from django.views.decorators.csrf import ensure_csrf_cookie
from .utils import generate_unique_title
from datetime import datetime
from calendar import monthrange
import json


import logging
logger = logging.getLogger(__name__)



class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            
            access_token = tokens['access']
            refresh_token = tokens['refresh']
            
            res = Response({'success': True})
            
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,  # Set to True if using HTTPS
                samesite='None',
                path='/',
            )
            res.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,  # Set to True if using HTTPS
                samesite='None',
                path='/',
            )
            
            return res
            
        except:
            return Response(
                {'success': False,},
                status=400
            )



class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'No refresh token'}, status=400)

        try:
            # request.data['refresh'] = refresh_token
            # response = super().post(request, *args, **kwargs)
            
            # tokens = response.data
            # access_token = tokens['access']
            # リクエストデータを明示的に置き換え
            mutable_data = request.data.copy()
            mutable_data['refresh'] = refresh_token
            request._full_data = mutable_data  # _full_data は裏技的（DRFの内部API）

            response = super().post(request, *args, **kwargs)
            access_token = response.data['access']
            
            res = Response({'refreshed': True})
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/',
            )
            return res
        
        except Exception as e:
            return Response({'error': str(e)}, status=400)

            
            
# ============ user ============
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def get_user(request):
    user = request.user
    serializer = UserGetSerializer(user, context={'request': request})
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def update_profile(request):
    user = request.user
    serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        print("serializer.validated_data:", serializer.validated_data)
        return Response({'success': True, 'data': serializer.data}, status=200)
    else:
        print("serializer.errors:", serializer.errors)
        return Response({'success': False, 'errors': serializer.errors}, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def update_password(request):
    serializer = PasswdUpdateSerializer(instance=request.user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success": True}, status=200)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@ensure_csrf_cookie
def logout(request):
    try:
        response = Response({'success': True}, status=200)
        response.delete_cookie('access_token', path='/')
        response.delete_cookie('refresh_token', path='/')
        return response
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=400)


@api_view(['POST'])
@ensure_csrf_cookie
@permission_classes([AllowAny])
def is_authenticated(request):
    is_auth = bool(getattr(request, 'user', None) and request.user.is_authenticated)
    return Response({ "authenticated": is_auth })



@api_view(['POST'])
@authentication_classes([])        # 認証を一切行わない
@permission_classes([AllowAny])   # 誰でもアクセス可
@ensure_csrf_cookie        
def register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(
        data={
            'success': True,
            'user_id': user.id,
            'user': serializer.data,
        },
        status=201
)
    return Response(serializer.errors, status=400)



# ============ note ============

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def get_notes(request):
    user = request.user
    notes = Note.objects.filter(owner=user)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def create_note(request):
    serializer = EntryNoteSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        note = serializer.save()
        return Response({'id': note.id, 'description': note.description}, status=201)
    return Response(serializer.errors, status=400)


# ============ weather ============

@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def weather_info(request):
    latlng = request.GET.get("latlng")
    if not latlng:
        return JsonResponse({"error": "need latlng parameter"}, status=400)

    try:
        lat, lng = map(float, latlng.split(","))
    except ValueError:
        return JsonResponse({"error": "format latlng incorrect. e.g.: 35.6895,139.6917"}, status=400)

    try:
        prefecture = get_address_from_latlng(lat, lng)
        weather_data = get_weather_info(prefecture)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({
        "success": True,
        "prefecture": prefecture,
         "weather": weather_data["weather"],
        "temperature": weather_data["temperature"]
    })
    


# ============ calendar ============

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def retrieve_calendar_event(request, event_id):
    try:
        event = CalendarEvent.objects.get(event_id=event_id, user=request.user)
        serializer = CalendarEventSerializer(event)
        return Response(serializer.data, status=200)
    
    except CalendarEvent.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def calendar_by_month(request):
    # クエリパラメータから取得
    year = int(request.query_params.get('year', datetime.now().year))
    month = int(request.query_params.get('month', datetime.now().month))

    # 月の開始日と終了日を取得
    start_date = datetime(year, month, 1).date()
    last_day = monthrange(year, month)[1]
    end_date = datetime(year, month, last_day).date()

    # フィルタリング：そのユーザーの、月内の予定
    events = CalendarEvent.objects.filter(
        user=request.user,
        date__range=(start_date, end_date)
    )

    serializer = CalendarEventSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def create_calendar_event(request):
    serializer = CalendarEventCreateSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        event = serializer.save()
        return Response({"message": "event registered", "event_id": event.event_id}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def update_calendar_event(request, event_id):
    try:
        event = CalendarEvent.objects.get(event_id=event_id, user=request.user)
    except CalendarEvent.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)
    
    serializer = CalendarEventUpdateSerializer(event, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def delete_calendar_event(request, event_id):
    try:
        event = CalendarEvent.objects.get(event_id=event_id, user=request.user)
        event.delete()
        return Response({'deleted': True}, status=204)
    except CalendarEvent.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)



# ============ immich ============
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def upload_images(request):
    files = request.FILES.getlist('images')
    if not files:
        return Response({"error": "No images uploaded."}, status=400)

    uploaded_ids = []
    for f in files:
        immich_id = upload_image_as_user(f, request.user)
        uploaded_ids.append(immich_id)

    return Response({"success": True, "uploaded": uploaded_ids}, status=201)



# ============ diary ============
@method_decorator(ensure_csrf_cookie, name="dispatch")
class EntryListView(generics.ListAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "body"]
    ordering_fields = ["created_at", "updated_at"]

    def get_queryset(self):
        user = self.request.user
        params = self.request.query_params

        is_public = params.get("public")
        start_date = params.get("start_date")
        end_date = params.get("end_date")

        # ベースクエリ
        queryset = Entry.objects.filter(is_public=True) if is_public == "true" else Entry.objects.filter(author=user)

        # 日時パースしてフィルター適用
        if start_date:
            parsed_start = parse_datetime(start_date)
            if parsed_start:
                queryset = queryset.filter(created_at__gte=parsed_start)

        if end_date:
            parsed_end = parse_datetime(end_date)
            if parsed_end:
                queryset = queryset.filter(created_at__lte=parsed_end)

        return queryset.order_by("-created_at")
    
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def create_entry_with_images(request):
    try:
        # --- ① 入力値取得 ---
        title = request.data.get("title")
        entry_date = request.data.get("entry_date")
        body = request.data.get("body", "")
        book_id = request.data.get("book_id")
        is_public = request.data.get("is_public", False)
        status_val = request.data.get("status", "draft")
        tags_raw = request.data.get("tags", "[]")
        files = request.FILES.getlist("images")

        if not title or not book_id:
            return Response({"error": "title および book_id は必須です。"}, status=400)

        try:
            tags = json.loads(tags_raw) if isinstance(tags_raw, str) else tags_raw
        except Exception:
            return Response({"error": "tagsの形式が不正です。JSON形式のリストを指定してください。"}, status=400)

        # --- ② Book 存在確認と所有者検証 ---
        try:
            book = DiaryBook.objects.get(id=book_id)
        except DiaryBook.DoesNotExist:
            return Response({"error": "指定された DiaryBook が存在しません。"}, status=404)
        if book.owner != request.user:
            return Response({"error": "この DiaryBook の所有者ではありません。"}, status=403)

        # --- ③ タイトルの重複チェックと補完 ---
        title = generate_unique_title(title, request.user)

        # --- ④ Entry 作成 ---
        entry = Entry.objects.create(
            book=book,
            entry_date=entry_date if entry_date else datetime.now().date(),
            author=request.user,
            title=title,
            body=body,
            is_public=is_public,
            status=status_val,
            tags=tags,
        )

        # --- ⑤ Immich に画像アップロード ---
        asset_ids = []
        for file in files:
            asset_id = upload_image_as_user(file, request.user)
            uuid.UUID(asset_id)
            if asset_id:  # Noneでない場合だけ追加
                EntryImages.objects.create(
                    owner=request.user,
                    entry=entry,
                    immich_asset_id=asset_id
                )
                asset_ids.append(asset_id)

        # --- ⑥ Immich アルバムに登録 ---
        if asset_ids:
            album_name = "entry"
            album = get_album_by_name(request.user, album_name)
            
            if album:
                album_id = album["id"]  # 既存アルバムに追加
                add_assets_to_album(request.user, album_id, asset_ids)
            else:
                # アルバムが存在しない → 新規作成（初回 asset_ids を含めて）
                create_album(
                    user=request.user,
                    album_name=album_name,
                    asset_ids=asset_ids,
                    description=entry.title
                )


        return Response({
            "entry_id": entry.id,
            "title": title,
            "book_id": str(book.id)
        }, status=201)

    except Exception as e:
        logger.error(f"Entry creation failed: {str(e)}")
        return Response({"error": str(e)}, status=500)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class EntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Entry.objects.all()
    serializer_class = EntrySerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        obj = super().get_object()
        # 所有者チェック
        if obj.author != self.request.user:
            raise PermissionError("このエントリーにアクセスする権限がありません。")
        return obj
    
    def update(self, request, *args, **kwargs):
        entry = self.get_object()
        data = request.data

        # --- 入力値の取得 ---
        title = data.get("title", entry.title)
        body = data.get("body", entry.body)
        is_public = data.get("is_public", entry.is_public)
        status_val = data.get("status", entry.status)
        tags_raw = data.get("tags", entry.tags)
        entry_date = data.get("entry_date", entry.entry_date)
        files = request.FILES.getlist("images")

        # --- JSON文字列形式のtagsならパース ---
        try:
            tags = json.loads(tags_raw) if isinstance(tags_raw, str) else tags_raw
        except Exception:
            return Response({"error": "tagsの形式が不正です。JSON形式のリストを指定してください。"}, status=400)

        # --- Entry を更新 ---
        entry.title = title
        entry.body = body
        entry.is_public = is_public
        entry.status = status_val
        entry.tags = tags
        entry.entry_date = entry_date
        entry.save()

        # --- 新規画像があればアップロード ---
        if files:
            asset_ids = []
            for file in files:
                asset_id = upload_image_as_user(file, request.user)
                uuid.UUID(asset_id)
                EntryImages.objects.create(
                    owner=request.user,
                    entry=entry,
                    immich_asset_id=asset_id
                )
                asset_ids.append(asset_id)

            # アルバムへ追加
            album_name = "entry"
            album = get_album_by_name(request.user, album_name)
            if album:
                album_id = album["id"]
                add_assets_to_album(request.user, album_id, asset_ids)
            else:
                create_album(
                    user=request.user,
                    album_name=album_name,
                    asset_ids=asset_ids,
                    description=entry.title
                )

        return Response({
            "entry_id": entry.id,
            "title": entry.title,
            "updated": True
        }, status=200)
        

    def delete(self, request, *args, **kwargs):
        entry = self.get_object()

        delete_images = request.query_params.get("delete_images", "false").lower() == "true"

        if delete_images:
            asset_ids = list(entry.images.values_list("immich_asset_id", flat=True))
            try:
                delete_assets_from_immich(request.user, asset_ids, force=True)
            except Exception as e:
                print(f"[Immich削除失敗]: {e}")
            entry.images.all().delete()

        entry.delete()
        return Response({"message": "エントリーと画像を削除しました。" if delete_images else "エントリーを削除しました。"}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def get_img_by_id(request, id):
    user = request.user
    headers = get_user_immich_auth_header(user)
    url = f"{IMMICH_BASE_URL}/api/assets/{id}/thumbnail"
    external_resp = requests.get(f"{IMMICH_BASE_URL}/api/assets/{id}/thumbnail", headers=headers)

    response = requests.get(url, headers=headers)
    return HttpResponse(
        external_resp.content,
        status=external_resp.status_code,
        content_type=external_resp.headers.get("Content-Type", "application/octet-stream")
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@ensure_csrf_cookie
def immich_asset_ids(request):
    """
    Immichのアセット一覧を取得するエンドポイント。
    """
    user = request.user
    headers = get_user_immich_auth_header(user)
    url = f"{IMMICH_BASE_URL}/api/search/metadata"

    # 1) デバイス AssetId のリストを取得
    try:
        resp = requests.post(url, headers=headers)
        resp.raise_for_status()
    except requests.HTTPError as e:
    # エラー内容をログに出す
        print("HTTP エラー:", e)

    # 2) Assets 一括取得エンドポイントを呼ぶ
    data = resp.json()      # ← 'data' は辞書として扱える
    items = data.get("assets", {}).get("items", [])
    id_list = [item.get("id") for item in items if "id" in item]
    return Response(id_list, status=200)