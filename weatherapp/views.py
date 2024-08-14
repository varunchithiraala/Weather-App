from django.shortcuts import render
from dotenv import load_dotenv
import os
import requests
import datetime

load_dotenv()

def home(request):
    # Set default city to Chennai
    city = 'Chennai'
    empty_city = False
    exception_occurred = False

    # Check if form is submitted
    if request.method == 'POST':
        city = request.POST.get('city', '').strip()
        
        # If input is empty, display error message
        if not city:
            empty_city = True
            return render(request, 'weatherapp/index.html', {
                'temp': '', 
                'city': '', 
                'description': '', 
                'icon': '', 
                'day': '', 
                'exception_occurred': exception_occurred, 
                'image_url': '',
                'empty_city': empty_city
            })

    # Load the API keys and IDs from environment variables
    APP_ID = os.getenv('APP_ID')
    API_KEY = os.getenv('API_KEY')
    SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
    
    # OpenWeatherMap API URL
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={APP_ID}'
    PARAMS = {'units': 'metric'}
    
    # Google Custom Search API URL
    query = city
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    # Fetch image URL
    image_data = requests.get(city_url).json()
    search_items = image_data.get("items", [])
    image_url = search_items[1]['link'] if search_items else 'https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600'

    try:
        # Fetch weather data
        data = requests.get(url, params=PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description, 
            'icon': icon, 
            'temp': temp, 
            'day': day, 
            'city': city, 
            'exception_occurred': exception_occurred, 
            'image_url': image_url,
            'empty_city': empty_city
        })

    except KeyError:
        # Display error message if the city is not valid
        exception_occurred = True
        return render(request, 'weatherapp/index.html', {
            'description': '', 
            'icon': '', 
            'temp': '', 
            'day': '', 
            'city': city, 
            'exception_occurred': exception_occurred, 
            'image_url': image_url,
            'empty_city': empty_city
        })
