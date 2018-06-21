
# coding: utf-8

# In[1]:


# website: https://www.washingtonpost.com/


# In[2]:


import requests
import pandas as pd
import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


# In[3]:


driver = webdriver.Chrome()
driver.get('https://www.washingtonpost.com/')


# In[38]:


recent_stories = []

content = driver.find_element_by_id('main-content')
stories = content.find_elements_by_class_name('moat-trackable')
for story in stories[1:7]:
    # this was breaking after 7 stories and I was feeling lazy.
    story_info = {}
    headline = story.find_element_by_class_name('headline')
    if headline:
        story_info['headline'] = headline.text
        print(headline.text)
    else:
        story_info['headline'] = ""
    link = story.find_element_by_tag_name('a').get_attribute('href')
    if link:
        story_info['link'] = link
        print(link)
    else:
        story_info['link'] = ""
    summary = story.find_element_by_class_name('blurb').text
    if summary:
        story_info['summary'] = summary
        print(summary)
    else:
        story_info['summary'] = ""     
    byline = story.find_element_by_class_name('byline')
    if byline:
        story_info['byline'] = byline
        print(byline.text)
    else:
        story_info['byline'] = ""

    recent_stories.append(story_info)


# In[39]:


right_now = datetime.datetime.now()
current_day = right_now.strftime("%A, %B %d")
current_time = right_now.strftime('%-I %p')
print(current_time, current_day)


# In[41]:


df = pd.DataFrame(recent_stories)
df


# In[42]:


filename = "washington-post" + right_now.strftime("%Y-%m-%d_%H_%M_%S") + ".csv"
df.to_csv(filename, index = False)


# In[43]:


subject_line = "Here is your " + current_time + " Daily Breifing for " + current_day
print(subject_line)
response = requests.post(
        "https://api.mailgun.net/v3/sandbox5b4ca76e82f54498a5cab0c622198844.mailgun.org/messages",
        auth=("api", "[API]"),
        files=[("attachment", open(filename))],
        data={"from": "<VERONICA_PENNEY@sandbox5b4ca76e82f54498a5cab0c622198844.mailgun.org>",
              "to": ["vp2400@columbia.edu", "t.burkel5758@gmail.com"],
              "subject": subject_line,
              "text": recent_stories}) 

