from django.urls import path, include
from api.views import UploadView

urlpatterns = [
    path(r'', UploadView.as_view(), name="upload_view"),
]
