# utils.py などに定義

from .models import Calendar, Entry

def get_default_calendar(user):
    calendar, _ = Calendar.objects.get_or_create(
        owner=user,
        name="マイカレンダー"
    )
    return calendar



def generate_unique_title(base_title, author):
    """
    著者ごとにタイトルの重複を避けるため、既存のタイトルと被らないよう自動補完。
    例: "My Title" → "My Title (2)", "My Title (3)", ...
    """
    title = base_title
    counter = 2
    while Entry.objects.filter(title=title, author=author).exists():
        title = f"{base_title} ({counter})"
        counter += 1
    return title