from django.urls import path
from . import views

urlpatterns = [
    # restful
    path('records', views.RecordList.as_view()),                        # records
    path('records/<int:record_id>', views.RecordDetail.as_view()),      
    path('arts', views.ArtList.as_view()),                              # arts
    path('arts/<int:art_id>', views.ArtDetail.as_view()),

    # other api
    path('submit/ticket', views.TicketSubmission.as_view()),                     # raw photo of poeple's handwriting
]