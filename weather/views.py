from django.shortcuts import render,loader
from django.http import HttpResponse,Http404,HttpResponseRedirect
import requests
from .models import City
from .forms import CityForm
from django.urls import reverse

import json
import datetime

url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=d0e6f5c09df2640c45908dd8a94daabe'	

def index(request):
	error_message=''
	if request.method == 'POST': # only true if form is submitted
		form = CityForm(request.POST) # add actual request data to form for processing
		print("form name ",form['name'].value())
		city_weather = requests.get(url.format(form['name'].value())).json() #request the API data and convert the JSON to Python data types
		
		print('-----cod=',city_weather['cod'])
		if city_weather['cod'] == '404':
				error_message="Invalid City/Country Name"
		else:
			error_message="City Successfully Added."			
			form.save() # will validate and save if validated
		context={'form':form,'error_message':error_message}	
		return(render(request,'weather/add_city.html',context))
	weather_data=[]
	
	cities = City.objects.all()
	print(cities)
	for city in cities:
		city_weather = requests.get(url.format(city.name)).json() #request the API data and convert the JSON to Python data types

		#Offline file which can be used while coding
		with open("sample.json", "w") as outfile: 
			json.dump(city_weather,outfile)

		#the offline json file
		# with open("sample.json", "r") as read_file:
		# 	city_weather = json.load(read_file)
		# read_file.close()

		# print(city_weather)

		#format of city_weather 
		# {'coord':{'lon': 12.2797, 'lat': 46.7406}, 
		# 	'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}],
		# 	 'base': 'stations',
		# 	 'main': {'temp': 39.2, 'feels_like': 33.01, 'temp_min': 39.2, 'temp_max': 39.2, 'pressure': 1021, 'humidity': 70},
		# 	 'visibility': 10000,
		# 	 'wind': {'speed': 9.22, 'deg': 130}, 
		# 	 'clouds': {'all': 0}, 
		# 	 'dt': 1620499213, 
		# 	 'sys': {'type': 1, 'id': 6829, 'country': 'IT', 'sunrise': 1620445529, 'sunset': 1620498556}, 
		# 	 'timezone': 7200,
		#	 'id': 3168508, 
		#	 'name': 'Innichen', 
		#	 'cod': 200}
		
		weather = {
			'city' : city.name,
			'temperature' : city_weather['main']['temp'],
			'description' : city_weather['weather'][0]['description'],
			'icon' : city_weather['weather'][0]['icon']
		}
		weather_data.append(weather)
	context = {
	'weather_data' : weather_data,
	'error_message':error_message}
	return render(request , 'weather/index.html', context) #returns the index.html template
def addCity(request):
	form = CityForm()
	context={'form':form}
	return render(request,'weather/add_city.html',context)


def cityDetails(request,city_name):
	city_weather = requests.get(url.format(city_name)).json() #request the API data and convert the JSON to Python data types
	
	timezone_offset=city_weather['timezone']#it is in seconds
	timezone_offset=datetime.timedelta(seconds=timezone_offset)	#convert to time format


	dt=city_weather['sys']['sunrise']
	sunrise = datetime.datetime.fromtimestamp(dt)	#UTC sunrise
	sunrise+=timezone_offset		#local time sunrise

	dt=city_weather['sys']['sunset']
	sunset= datetime.datetime.fromtimestamp(dt)
	sunset+=timezone_offset

	coordinates=city_weather['coord']
	main=city_weather['main']
	wind=city_weather['wind']
	sun=city_weather['sys']
	weatherdata=city_weather['weather'][0]
	context={
	'coordinates':coordinates,
	'city_name':city_name,
	'weather':weatherdata,
	'main':main,
	'wind':wind,
	'sun':sun,
	'sunrise':sunrise,
	'sunset':sunset
	}
	return render(request,'weather/city_detail.html',context)
#src of icon img
#src="{% static '/' weather.icon %}"