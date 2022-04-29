from django.urls import path
from . import views

urlpatterns = [
    path('records', views.RecordList.as_view()),
    path('records/<int:record_id>', views.RecordDetail.as_view()),
    path('arts', views.ArtList.as_view()),
    path('arts/<int:art_id>', views.ArtDetail.as_view()),
]