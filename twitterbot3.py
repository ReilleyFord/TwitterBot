import tweepy, time, sys
import pyowm
from datetime import datetime, timedelta
from pytz import timezone
import pytz


#enter the corresponding information from your Twitter application:
OpenWeatherMap = pyowm.OWM('your OWM API key')
CONSUMER_KEY = 'your twitter consumer API key'
CONSUMER_SECRET = 'your twitter consumer secret API key'
ACCESS_KEY = 'your twitter access API key'
ACCESS_SECRET = 'your twitter access secret API key'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#setting the timezone to my local timezone. If i don't specifically set it to my
#timezone and i use localdate then it will use the timezone from the heroku server
#that i'm using, which is wrong.
eastern = pytz.timezone('US/Eastern')
dateFormat = '%I:%M %p'
localdt = datetime.now(eastern)
dateStr = localdt.strftime(dateFormat)

#scraping data from openweathermap with pyowm import
observation = OpenWeatherMap.weather_at_id(6167865)
weather = observation.get_weather()

#simple function to get the temp and format it.
def getTemp():
    temp = str(weather.get_temperature('celsius'))
    temp = temp.replace('temp_kf: None', '')
    temp = temp.replace('{', '')
    temp = temp.replace('}', '')
    temp = temp.replace('\'', '')
    temp = temp.replace('temp_max', '')
    temp = temp.replace('temp_min', '')
    temp = temp.replace('temp', '')
    temp = temp.replace(':', '')
    temp = temp.replace(' ','')
    temp = temp.split(',', 1)
    temp = temp[0]
    return temp

#While loop looping once every two hours.
while True:
    newTemp = getTemp()
    api.update_status(".@ReilleyFord The time is: " + dateStr +  "\nThe temperature in Barrie is: " + newTemp + '°')
    time.sleep(7200)
    