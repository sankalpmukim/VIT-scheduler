from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('index/', views.IndexView.as_view(), name='index'),
    path('', views.test_form, name='form'),
    path('test_result/', views.test_result, name='result'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('<str:filepath>/', views.download_file, name='download'),
]
