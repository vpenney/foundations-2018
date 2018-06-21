
# coding: utf-8

# In[1]:


import requests
import datetime
import pandas as pd


# In[2]:


response = requests.get('https://api.darksky.net/forecast/[API key]/40.796517,-73.9639937')
manhattan = response.json()
print(manhattan.keys())


# In[3]:


current = manhattan['currently']


# In[4]:


temperature = current['temperature']
summary = current['summary'].lower()
forecast = manhattan['daily']['data']
today = forecast[0]
rain_warning = ''


if today['temperatureHigh'] > 80:
    temp_feeling = 'toasty hot'
elif today['temperatureHigh'] > 60:
    temp_feeling = 'pleasantly warm'
else:
    temp_feeling = 'rather cold'

high_temp = today['temperatureHigh']
high_temp_time = datetime.datetime.fromtimestamp(today['temperatureHighTime']).strftime('%H:%M')

low_temp = today['temperatureLow']

if today['precipProbability'] > 40:
    rain_warning = 'A rain jacket would be a wise move today.'
else:
    pass

weather_today = "Right now it is {} degrees outside and {}. Today will be {} with a high of {} at {} and a low of {}. {}".format(temperature, summary, temp_feeling, high_temp, high_temp_time, low_temp, rain_warning)
print(weather_today)


# 
# 

# In[5]:


rows = []

weather_report = {}

weather_report['temperature'] = current['temperature']
weather_report['summary'] = current['summary'].lower()
forecast = manhattan['daily']['data']
today = forecast[0]
rain_warning = ''

if today['temperatureHigh'] > 80:
    weather_report['temp_feeling'] = 'toasty hot'
elif today['temperatureHigh'] > 60:
    weather_report['temp_feeling'] = 'pleasantly warm'
else:
    weather_report['temp_feeling'] = 'rather cold'

weather_report['high_temp'] = today['temperatureHigh']
weather_report['high_temp_time'] = datetime.datetime.fromtimestamp(today['temperatureHighTime']).strftime('%-I %p')

weather_report['low_temp'] = today['temperatureLow']

if today['precipProbability'] > 40:
    weather_report['rain_warning'] = 'A rain jacket would be a wise move today.'
else:
    pass

rows.append(weather_report)
print(rows)


# In[10]:


right_now = datetime.datetime.now()
date_string = right_now.strftime("%Y-%M")
current_day = right_now.strftime("%A, %B %d")
current_time = right_now.strftime('%-I %p')
print(current_time, current_day)


# In[7]:


df = pd.DataFrame(rows)
filename = "dark_sky-" + right_now.strftime("%Y-%m-%d_%H_%M_%S") + ".csv"
df


# In[12]:


df.to_csv("dark_sky.csv", index = False)


# In[14]:


import requests
subject_line = current_time + " Weather Forecast: " + current_day
response = requests.post(
        "https://api.mailgun.net/v3/sandbox5b4ca76e82f54498a5cab0c622198844.mailgun.org/messages",
        auth=("api", "[my API]"),
        data={"from": "<VERONICA_PENNEY@sandbox5b4ca76e82f54498a5cab0c622198844.mailgun.org>",
              "to": "vp2400@columbia.edu",
              "subject": subject_line,
              "text": weather_today}) 

