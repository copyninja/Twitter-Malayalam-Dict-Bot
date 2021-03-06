#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# eng-mal-bot.py A Twitter bot which provide eng-mal dictionary lookup service
#       
# Copyright (c) 2010
#	 Ershad K <ershad92@gmail.com>
#    Hrishikesh K B <hrishi.kb@gmail.com>
#
# Swathanthra Malayalam Computing(http://smc.org.in/)
#       
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#       
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import os, sys, codecs
import time
import tweepy
from dictdlib import DictDB

# Change the following values
sleep_time = 1 


fout = open('dataFile', 'a') #to create such a file
fout.close()

#OAuth
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

while True:
	time.sleep(sleep_time)
	sleep_time = 200 #To make it more twitter-server friendly
	word = ''
	timeline = api.mentions()
	for s in timeline:
		dict_keyword_find = -1
		check_duplicate = 0;
		print "%s --> %s" % (s.user.screen_name, s.text)


		tweet = s.user.screen_name + "\t" + s.text
		dict_keyword_find = tweet.find("dict") 

		if dict_keyword_find > 0:
			fin = open('dataFile', 'r')
			fin_contents = fin.read()
			check_duplicate = fin_contents.find(str(s.id))
			print check_duplicate
			fin.close()
	
		if check_duplicate < 0:
			print "%s --> %s" % (s.user.name, s.text)
			word = s.text[13:]
			print word #for debugging			
			en_ml_db = DictDB("freedict-eng-mal")
			try:
				definition = en_ml_db.getdef(word)[0]
			except:	
				definition =  "No definitions found"
			print definition
			defi = definition [0:110]
		
			output = '@' + s.user.screen_name + ' '
			output = output +  unicode(defi,'utf-8')
			#output = '@' + s.user.screen_name + " Request recieved."
			#print len(output)
			print output     
			api.update_status(output)
			fout = open('dataFile', 'a')
			text = '\n' #To write each status id in a new line
			text = text + str(s.id)
			fout.write(text)
			fout.close()
