from django.urls import path, include
from api.views import UploadView, GamesView, GamesDetailedView

urlpatterns = [
    path('upload', UploadView.as_view(), name="upload_view"),
    path('games', GamesView.as_view(), name="games_view"),
    path('games/<pk>', GamesDetailedView.as_view(), name='games_detailed_view')
]
