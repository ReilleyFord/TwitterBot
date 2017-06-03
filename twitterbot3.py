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

#setting the timezone to my local timezone. Otherwise it will grab it serverside.
eastern = pytz.timezone('US/Eastern')
dateFormat = '%I:%M %p'
localdt = datetime.now(eastern)
dateStr = localdt.strftime(dateFormat)

#scraping data from openweathermap with pyowm import support for Barrie and Orillia
barrieObserv = OpenWeatherMap.weather_at_id(6167865)
orilliaObserv = OpenWeatherMap.weather_at_coords(44.61,-79.42)
weather = orilliaObserv.get_weather()
count = 0
#looping infinitely and sleeping for 30 seconds per timeline scrape
while True:
	#grabbing the temp dict and using the avg temp key
	def getTemp():
		temp = (weather.get_temperature('celsius'))
		return ('%.2f' % temp["temp"])

	def getStatus():
		lastStatuses = api.home_timeline(screen_name = 'ReilleyFord', count = 1)
		for status in lastStatuses:
			tweet = status._json
			tweet = tweet["text"]
			sendTweet(tweet.lower())

	def sendTweet(tweet):
		if("weather" in tweet):
			try:
				api.update_status(".@ReilleyFord The time is: " + dateStr +
				"\nThe temperature in Orillia is: " + getTemp() + '°')
			except (tweepy.error.RateLimitError, tweepy.error.TweepError):
				pass

	def favBot():
		try:
			findSelfTweets = api.home_timeline(screen_name = 'ReilleyFord', count = 1)
			for tweet in findSelfTweets:
				selfTweet = tweet._json
				selfTweet = selfTweet['user']['screen_name']
			if('ReilleyFord' in selfTweet):
				tweetList = tweet._json
				tweetID = tweetList['id']
				api.create_favorite(tweetID)
		except (tweepy.TweepError, tweepy.RateLimitError):
			pass

	favBot()
	getStatus()
	time.sleep(45)
