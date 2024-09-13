# urls.py
from django.urls import path
from core.views import SensorDataView, AggregatedDataView, SensorDataCSVUploadView, RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('sensor-data', SensorDataView.as_view(), name='sensor-data'),
    path('upload-csv', SensorDataCSVUploadView.as_view(), name='sensor-data-csv-upload'),
    path('aggregated-data', AggregatedDataView.as_view(), name='aggregated-data'),
    path('register', RegisterView.as_view(), name='register'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
