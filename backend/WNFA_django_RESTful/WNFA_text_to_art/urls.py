from django.urls import path
from . import views

urlpatterns = [
    path('records', views.RecordList.as_view()),
    path('records/<record_id>', views.RecordDetail.as_view()),
]