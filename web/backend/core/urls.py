from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('datalist',
         views.DataList.as_view(),
         name='DataList'),
    path('hello',
         views.HellowView.as_view(),
         name='hello'),
]