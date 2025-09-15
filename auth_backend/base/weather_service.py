import os
import requests
from django.conf import settings

api_key = settings.GOOGLE_API_KEY

# 都道府県名と気象庁の予報区コードのマッピング
JMA_AREA_CODES = {
    "北海道": "016000",
    "青森県": "020000",
    "岩手県": "030000",
    "宮城県": "040000",
    "秋田県": "050000",
    "山形県": "060000",
    "福島県": "070000",
    "茨城県": "080000",
    "栃木県": "090000",
    "群馬県": "100000",
    "埼玉県": "110000",
    "千葉県": "120000",
    "東京都": "130000",
    "神奈川県": "140000",
    "新潟県": "150000",
    "富山県": "160000",
    "石川県": "170000",
    "福井県": "180000",
    "山梨県": "190000",
    "長野県": "200000",
    "岐阜県": "210000",
    "静岡県": "220000",
    "愛知県": "230000",
    "三重県": "240000",
    "滋賀県": "250000",
    "京都府": "260000",
    "大阪府": "270000",
    "兵庫県": "280000",
    "奈良県": "290000",
    "和歌山県": "300000",
    "鳥取県": "310000",
    "島根県": "320000",
    "岡山県": "330000",
    "広島県": "340000",
    "山口県": "350000",
    "徳島県": "360000",
    "香川県": "370000",
    "愛媛県": "380000",
    "高知県": "390000",
    "福岡県": "400000",
    "佐賀県": "410000",
    "長崎県": "420000",
    "熊本県": "430000",
    "大分県": "440000",
    "宮崎県": "450000",
    "鹿児島県": "460100",
    "沖縄県": "471000"
}

def extract_prefecture(geocode_data: dict) -> str | None:
    results = geocode_data.get("results", [])
    if not results:
        return None

    for component in results[0].get("address_components", []):
        if "administrative_area_level_1" in component.get("types", []):
            return component.get("long_name")

    return None

def get_address_from_latlng(lat, lng):
    response = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json",
        params={"latlng": f"{lat},{lng}", "language": "ja", "key": api_key}
    )

    data = response.json()
    #print(data)  # デバッグ用にレスポンスを表示
    prefecture = extract_prefecture(data)

    if prefecture is None:
        raise ValueError("都道府県を取得できませんでした")

    return prefecture

def get_weather_info(prefecture):
    area_code = JMA_AREA_CODES.get(prefecture)
    if not area_code:
        raise Exception(f"{prefecture} に対応する気象庁のエリアコードが見つかりません。")

    forecast_url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
    response = requests.get(forecast_url)
    if response.status_code != 200:
        raise Exception("気象庁の天気予報データの取得に失敗しました。")

    data = response.json()
    try:
        # 天気情報の取得
        weather = data[0]["timeSeries"][0]["areas"][0]["weathers"][0]

        # 気温情報の取得
        # temps = data[0]["timeSeries"][0]["areas"][0]
        # temp_min = temps.get("tempsMin", [""])[0]
        # temp_max = temps.get("tempsMax", [""])[0]
        
        temps_data = data[1]["timeSeries"][1]["areas"]
        temp_min = temp_max = None

        for area in temps_data:
            if area["area"]["name"] in ["東京", prefecture.replace("都", "").replace("府", "").replace("県", "")]:
                temp_min = area.get("tempsMin", [""])[1]
                temp_max = area.get("tempsMax", [""])[1]
                break

        temperature = ""
        if temp_min and temp_max:
            temperature = f"{temp_min}℃〜{temp_max}℃"
        elif temp_max:
            temperature = f"{temp_max}℃"
        elif temp_min:
            temperature = f"{temp_min}℃"

        return {
            "weather": weather,
            "temperature": {
                "min": f"{temp_min}℃" if temp_min else None,
                "max": f"{temp_max}℃" if temp_max else None
            }
        }
    except (KeyError, IndexError):
        raise Exception("天気情報の解析に失敗しました。")
