import tweepy, time, sys
import pyowm
from datetime import datetime, timedelta
from pytz import timezone
import pytz


#enter the corresponding information from your Twitter application API
#and your OpenWeatherMap API key
OpenWeatherMap = pyowm.OWM('your OWM API key')
CONSUMER_KEY = 'your twitter consumer API key'
CONSUMER_SECRET = 'your twitter consumer secret API key'
ACCESS_KEY = 'your twitter access API key'
ACCESS_SECRET = 'your twitter access secret API key'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

#setting the timezone to my local timezone. If i don't specifically set it to my
#timezone and i use localdate then it will use the timezone from the server
#that i'm using, which is not EST.
eastern = pytz.timezone('US/Eastern')
dateFormat = '%I:%M %p'
localdt = datetime.now(eastern)
dateStr = localdt.strftime(dateFormat)

#scraping data from openweathermap with pyowm import support for Barrie and Orillia
barrieObserv = OpenWeatherMap.weather_at_id(6167865)
orilliaObserv = OpenWeatherMap.weather_at_coords(44.61,-79.42)
weather = orilliaObserv.get_weather()

#grabbing the temp dict and using the avg temp key
def getTemp():
    temp = (weather.get_temperature('celsius'))
    return ('%.2f' % temp["temp"])

#looping infinitely and sleeping for four hours at a time.
while True:
    temp = getTemp()
    api.update_status(".@ReilleyFord The time is: " + dateStr + "\nThe temperature in Orillia is: " + temp + '°')
    time.sleep(14400)

    