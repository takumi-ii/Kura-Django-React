from django.urls import path

from .views import (
    get_notes, 
    CustomTokenObtainPairView, 
    CookieTokenRefreshView, 
    EntryDetailView,
    EntryListView,
    logout, 
    is_authenticated, 
    register, 
    weather_info, 
    get_user, 
    update_profile,
    update_password, 
    create_note,
    retrieve_calendar_event,
    calendar_by_month,
    create_calendar_event,
    update_calendar_event,
    delete_calendar_event,
    upload_images,
    create_entry_with_images,
    get_img_by_id,
    immich_asset_ids
    )

urlpatterns = [
    # ======= user ========
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('authenticated/', is_authenticated, name='is_authenticated'),
    path('user/update_password/', update_password, name='update_password'),
    
    path('user/profile/', get_user, name='get_user'),
    path("user/profile/update/", update_profile, name="update_profile"),
    
    # ======= note ========
    path('notes/', get_notes, name='user_notes'),
    path('notes/create/', create_note, name='create_note'),
    
    # ======= weather ========
    path('weather/', weather_info, name='weather_info'),
    
    # ======= calendar ========
    path('calendar/<uuid:event_id>/', retrieve_calendar_event, name='calendar-detail'),
    path('calendar/month/', calendar_by_month, name='calendar_by_month'),
    path('calendar/create/', create_calendar_event, name='calendar_create'),
    path('calendar/update/<uuid:event_id>/', update_calendar_event, name='update_calendar_event'),
    path('calendar/delete/<uuid:event_id>/',delete_calendar_event, name='delete_calendar_event'),
    
    # ======= immich ========
    path('images/upload/', upload_images, name='upload_images'),
    path("diary/image/<uuid:id>/thumbnail/", get_img_by_id, name="get_img_by_id"),
    path('photos/assets/', immich_asset_ids, name="immich_asset_ids"),
     
    # ======= diary ========
    path("diary/entries/", EntryListView.as_view(), name="entry-list"),
    path("diary/entry/", create_entry_with_images, name="entry-create-with-images"),
    path('diary/entry/<uuid:pk>/', EntryDetailView.as_view(), name='entry'),

    
]