import tweepy, time, sys
import pyowm
from datetime import datetime, timedelta
from pytz import timezone
import pytz

#enter the corresponding information from your Twitter application API
#and your OpenWeatherMap API key
OpenWeatherMap = pyowm.OWM('yourKey')
CONSUMER_KEY = 'yourKey'
CONSUMER_SECRET = 'yourKey'
ACCESS_KEY = 'yourKey'
ACCESS_SECRET = 'yourKey'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = 'true', wait_on_rate_limit_notify = 'true')

#setting the timezone to my local timezone. Otherwise it will grab it serverside.
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

def getStatus():
	lastStatuses = api.home_timeline(count = 1)
	for status in lastStatuses:
		tweet = status.text
		print("Found Status: " + tweet)
		return(tweet)

def getScreenName():
	lastStatuses = api.home_timeline(count = 1)
	for status in lastStatuses:
		tweet = status.user
		screenName = tweet.screen_name
		print("Found Screen Name: " + screenName)
		return(screenName)

def getTweetId():
	lastStatuses = api.home_timeline(count = 1)
	for status in lastStatuses:
		tweet = status.id
		print("Found Tweet #: ", tweet)
		return(tweet)

def sendWeatherReport(tweet):
	try:
		api.update_status(".@ReilleyFord The time is: " + dateStr +
		"\nThe temperature in Orillia is: " + getTemp() + '°')
		print("Tweet Sent")
	except (tweepy.error.RateLimitError, tweepy.error.TweepError):
		pass

def favTweet(favTweet):
	try:
		api.create_favorite(favTweet)
		print("Tweet Favourited: ", favTweet)
	except (tweepy.TweepError, tweepy.RateLimitError):
		pass

#looping infinitely and sleeping for 60 seconds per timeline scrape
while True:
	if('weather' in getStatus()):
		sendWeatherReport(getStatus)
	if(getScreenName() == 'ReilleysTesting'):
		favTweet(getTweetId())
	print("Sleeping")
	time.sleep(60)
