from django.urls import path
from . import views
urlpatterns = [
	path('',views.index,name='index'),
	path('addcity/',views.addCity,name='addCity'),
	path('<str:city_name>/',views.cityDetails,name='cityDetails')
]