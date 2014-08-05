#this script gets creates an XML document with the current users connections
#and using the id tags will create a text file of updates for each person

import oauth2 as oauth
import httplib2
import time, os, simplejson
import urlparse
import datetime
from xml.dom import minidom


#praful tokens
"""
Company: DerivativeD
Application Name: SalesProspecter
"""
API_KEY = '77q4z49z65kqxt'
API_SECRET = 'XHRn8XZ8jSHzDah7'
OAUTH_TOKEN = '8c65e1b6-2847-443b-a602-b6ee382049d0'
OAUTH_TOKEN_SECRET = 'e1291200-1129-4019-924e-78e4e698bd74'

#instantiate objects to begin calls
consumer = oauth.Consumer(API_KEY, API_SECRET)
access_token = oauth.Token(key=OAUTH_TOKEN, secret=OAUTH_TOKEN_SECRET)
client = oauth.Client(consumer, access_token)

#get xml doc of connections
url = "http://api.linkedin.com/v1/people/~/connections:(id,first-name,last-name)"
resp,content = client.request(url)


url = "http://api.linkedin.com/v1/people/id=%s/network/updates?scope=self" %ids[i]
resp,content = client.request(url)
