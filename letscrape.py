from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from StringIO import StringIO
import pandas as pd
import re,datetime,json
import mechanize
import time
import requests
import pycurl

class letscrape(object):
	#Get Source of the Website
	def getSource(self):
		browser = webdriver.Firefox()
		browser.get('http://www.google.com')
		print browser.page_source
		re.sub('<[^>]*>', '', browser.page_source)

	#Get list of Stocks on Quandl
	def getquandlstocklist(self):
		print "Scraping Quandl"		
		browser = webdriver.Firefox()
		stock_list = []
		pages_to_parse = 1
		for pages in range(pages_to_parse):
			browser.get('https://www.quandl.com/data/NSE?keyword=&page='+str(pages))
			time.sleep(5)
			i = 0
			while(i<2):				#Working
				title = browser.find_elements_by_xpath('//span[contains(@class,"ember-view")]')[i].text
				stock_list.append(title)
				print title
				i+=1

		df = pd.DataFrame(stock_list)  
		df.to_csv("stocklist_csvs/stock"+format(datetime.datetime.now())+".csv", sep='\t')
		return stock_list

	def getdataquandl(self,stock_list):
		#https://www.quandl.com/api/v3/datasets/NSE/20MICRONS.json
		buffer = StringIO()
		for stocks in stock_list:
			print "Getting Data for",stocks
			c = pycurl.Curl()
			c.setopt(c.URL, 'https://www.quandl.com/api/v3/datasets/'+stocks+'.json')
			c.setopt(c.WRITEDATA, buffer)
			c.perform()
			c.close()
			data = buffer.getvalue()
			with open("data_jsons/stock"+format(datetime.datetime.now())+".json", 'w') as outfile:
				json.dump(data, outfile)		
		


scrap_obj = letscrape()
stock_list = scrap_obj.getquandlstocklist()
scrap_obj.getdataquandl(stock_list)