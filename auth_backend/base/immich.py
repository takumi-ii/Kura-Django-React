from django.conf import settings
import requests
import datetime
import uuid
from pathlib import Path
from django.utils.timezone import make_aware

IMMICH_EMAIL = settings.IMMICH_ADMIN_EMAIL
IMMICH_PASS = settings.IMMICH_ADMIN_PASS

IMMICH_BASE_URL = "http://192.168.0.124:2283"

IMMICH_LOGIN_URL = f"{IMMICH_BASE_URL}/api/auth/login"
IMMICH_UPLOAD_URL = f"{IMMICH_BASE_URL}/api/assets"

def get_file_times(file_obj):
    try:
        path = Path(file_obj.temporary_file_path())
    except Exception:
        raise Exception("ファイルがディスクに保存されていないため、タイムスタンプを取得できません")

    if not path.exists():
        raise Exception(f"パスが存在しません: {path}")

    stat = path.stat()
    created_at = datetime.datetime.fromtimestamp(stat.st_ctime)
    modified_at = datetime.datetime.fromtimestamp(stat.st_mtime)

    # aware にする（ImmichがUTC前提の可能性があるため）
    created_at = make_aware(created_at)
    modified_at = make_aware(modified_at)

    return created_at.isoformat(), modified_at.isoformat()


def get_immich_token(email, password):
    res = requests.post(IMMICH_LOGIN_URL, json={"email": email, "password": password})
    if res.status_code != 201:
        raise Exception(f"Immich login failed: {res.status_code} - {res.text}")
    return res.json()["accessToken"]


def get_user_immich_auth_header(user):
    if user.immich_pat:
        # PAT が存在する場合はそれを使う
        return {"Authorization": f"Bearer {user.immich_pat}"}
    elif user.immich_email and user.immich_password:
        # PAT がなければ Email + Password でトークン取得
        token = get_immich_token(user.immich_email, user.immich_password)
        return {"Authorization": f"Bearer {token}"}
    else:
        raise Exception("No valid Immich authentication method configured for user.")


def upload_image_as_user(file, user):
    headers = get_user_immich_auth_header(user)

    file_created_at, file_modified_at = get_file_times(file)
    file_content = file.read()

    files = {
        "assetData": (file.name, file_content, file.content_type),
    }
    data = {
        "deviceAssetId": str(uuid.uuid4()),
        "deviceId": "django-backend",
        "fileCreatedAt": file_created_at,
        "fileModifiedAt": file_modified_at,
        "visibility": "timeline"
    }

    res = requests.post(IMMICH_UPLOAD_URL, headers=headers, files=files, data=data)

    if res.status_code not in (200, 201):
        raise Exception(f"Upload failed for '{file.name}': {res.status_code} - {res.text}")

    res_json = res.json()

    if "id" not in res_json:
        raise Exception(f"Upload response missing 'id' for '{file.name}': {res_json}")

    return res_json["id"]



def create_album(user, album_name, asset_ids, album_users=None, description=None):
    headers = get_user_immich_auth_header(user)
    payload = {
        "albumName": album_name,
        "assetIds": asset_ids,
    }

    if album_users:
        payload["albumUsers"] = album_users

    if description:
        payload["description"] = description

    url = f"{IMMICH_BASE_URL}/api/albums"
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 201:
        raise Exception(f"アルバム作成失敗: {response.status_code} - {response.text}")

    album_data = response.json()

    # ImmichのアルバムIDをユーザーモデルに保存（任意: 一度だけ作成を想定）
    if not user.immich_entry_album_id:
        user.immich_entry_album_id = album_data.get("id")
        user.save(update_fields=["immich_entry_album_id"])

    return album_data


def get_album_by_name(user, album_name):
    """
    Immich に存在するアルバムの一覧を取得し、指定名のアルバムがあるかを探す。
    見つかればアルバム情報（dict）を返す。なければ None。
    """
    headers = get_user_immich_auth_header(user)
    url = f"{IMMICH_BASE_URL}/api/albums"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"アルバム一覧取得失敗: {response.status_code} - {response.text}")

    for album in response.json():
        if album.get("albumName") == album_name:
            return album
    return None

def add_assets_to_album(user, album_id, asset_ids):
    """
    指定された album_id に画像を追加する。
    """
    headers = get_user_immich_auth_header(user)
    url = f"{IMMICH_BASE_URL}/api/albums/{album_id}/assets"

    payload = {"ids": asset_ids}

    response = requests.put(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"アルバムへの追加失敗: {response.status_code} - {response.text}")

    return response.json()



def delete_assets_from_immich(user, asset_ids, force=True):
    """
    複数の Immich アセットを一括削除する
    :param user: Django user (CustomUser) インスタンス
    :param asset_ids: 削除する asset_id のリスト（UUID文字列）
    :param force: 完全削除フラグ（True = ゴミ箱を使わず削除）
    """
    if not asset_ids:
        return

    headers = get_user_immich_auth_header(user)
    url = f"{IMMICH_BASE_URL}/api/assets"

    payload = {
        "force": force,
        "ids": asset_ids,
    }

    response = requests.delete(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"Immich アセット一括削除失敗: {response.status_code} - {response.text}")
